from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Event, Organization
from core.serializers import EventSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import PermissionDenied
from datetime import timedelta, datetime


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Event.objects.all()
        perks = self.request.query_params.get('perks')
        table_size = self.request.query_params.get('table_size')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        visibility = self.request.query_params.get('visibility')

        if perks:
            perks_list = [p.strip() for p in perks.split(',')]
            for perk in perks_list:
                queryset = queryset.filter(perks__icontains=perk)

        if table_size:
            queryset = queryset.filter(table_size=table_size)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if start_date:
            queryset = queryset.filter(start_time__date=start_date)

        if visibility:
            queryset = queryset.filter(visibility=visibility)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        org_id = self.request.data.get("organization")

        try:
            organization = Organization.objects.get(id=org_id)
            if organization.created_by != user and user not in organization.members.all():
                raise PermissionError("User does not belong to this organization")
        except Organization.DoesNotExist:
            raise ValueError("Selected organization does not exist")

        # Pagrindinio įvykio sukūrimas
        base_event = serializer.save(created_by=user, organization=organization)

        # Automatiškai pridedame kūrėją kaip dalyvį, jei first_player_is_organizer == False
        if not base_event.first_player_is_organizer:
            base_event.players.add(user)
            base_event.organizers.add(user)
            base_event.save()

        # Repeat logic - patobulinta versija
        if base_event.is_repeating and base_event.repeat_days:
            repeat_dates = base_event.repeat_days.split(',')

            # Išsaugome trukmę ir laikus
            base_start_time = base_event.start_time.time()
            base_end_time = base_event.end_time.time()
            base_duration = base_event.end_time - base_event.start_time

            for date_str in repeat_dates:
                try:
                    # Skiriame datų stringus nuo kitų formatų
                    date_str = date_str.strip()
                    if not date_str:
                        continue

                    # Konvertuojame į datą
                    try:
                        # Bandome ISO formatą YYYY-MM-DD
                        date_obj = datetime.fromisoformat(date_str).date()
                    except Exception:
                        try:
                            # Bandome alternatyvų formatą
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except Exception:
                            print(f"Nepavyko konvertuoti datos {date_str}")
                            continue

                    # Jei ši data sutampa su pagrindinio įvykio data, praleidžiame
                    if date_obj == base_event.start_time.date():
                        continue

                    # Sukuriame naują pradžios ir pabaigos laiką
                    from django.utils import timezone

                    # Panaudojame datetime.combine, kad sukurtume naują datetima objektą
                    # su pasirinkta data ir originalios datos laiku
                    naive_start = datetime.combine(date_obj, base_start_time)
                    naive_end = datetime.combine(date_obj, base_end_time)

                    # Jei pabaigos laikas yra mažesnis už pradžios laiką (t.y. kito ryto),
                    # pridedame dieną prie pabaigos laiko
                    if naive_end < naive_start:
                        naive_end += timedelta(days=1)

                    # Jei Django naudoja aware datetime (USE_TZ=True), konvertuojame į aware
                    if timezone.is_aware(base_event.start_time):
                        start_time = timezone.make_aware(naive_start)
                        end_time = timezone.make_aware(naive_end)
                    else:
                        start_time = naive_start
                        end_time = naive_end

                    # Sukuriame naują įvykį
                    repeated_event = Event.objects.create(
                        title=base_event.title,
                        description=base_event.description,
                        address=base_event.address,
                        table_size=base_event.table_size,
                        perks=base_event.perks,
                        start_time=start_time,
                        end_time=end_time,
                        is_repeating=False,
                        visibility=base_event.visibility,
                        created_by=user,
                        organization=organization,
                        first_player_is_organizer=base_event.first_player_is_organizer,
                    )

                    # Jei first_player_is_organizer yra False, iš karto pridedame kūrėją
                    # kaip organizatorių ir žaidėją prie pasikartojančių įvykių
                    if not base_event.first_player_is_organizer:
                        repeated_event.players.add(user)
                        repeated_event.organizers.add(user)
                        repeated_event.save()

                except Exception as e:
                    print(f"Error creating repeated event: {e}")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Naudojame join_player metodą iš Event modelio,
        # kuris apdoroja ir first_player_is_organizer logiką
        success = event.join_player(user)

        if success:
            return Response({'detail': 'Prisijungta prie renginio sėkmingai.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Jau esate prisijungęs prie šio renginio.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        # Tikrinti ar vartotojas turi teisę redaguoti
        is_creator = event.created_by == user
        is_organizer = event.organizers.filter(id=user.id).exists()

        if not (is_creator or is_organizer):
            raise PermissionDenied("Tik renginio kūrėjas arba organizatoriai gali redaguoti renginį.")

        # Gaukime pradinių duomenų kopiją
        mutable_data = request.data.copy()

        # Visais atvejais neleidžiame redaguoti žaidėjų ir organizatorių sąrašo
        mutable_data.pop('players', None)
        mutable_data.pop('organizers', None)

        # Jei vartotojas yra organizatorius, bet ne kūrėjas, ir tapo organizatoriumi per "pirmas prisijungęs" funkciją
        if is_organizer and not is_creator and event.first_player_is_organizer:
            # Leidžiame redaguoti tik pavadinimą, aprašymą ir viešumą
            allowed_fields = ['title', 'description', 'visibility']

            # Pašaliname visus kitus laukus
            data_keys = list(mutable_data.keys())
            for key in data_keys:
                if key not in allowed_fields:
                    mutable_data.pop(key, None)

        # Naudojam serializerį su išvalytais duomenimis
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(event, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)