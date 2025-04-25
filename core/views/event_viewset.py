from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Event, Organization
from core.serializers import EventSerializer
from django.utils.dateparse import parse_datetime
from datetime import timedelta

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

        base_event = serializer.save(created_by=user, organization=organization)

        # ✅ Automatiškai pridedame kūrėją kaip dalyvį, jei first_player_is_organizer == False
        if not base_event.first_player_is_organizer:
            base_event.players.add(user)
            if not base_event.actual_organizer:
                base_event.actual_organizer = user
            base_event.save()

        # Repeat logic (nekeičiamas)
        if base_event.is_repeating and base_event.repeat_days:
            repeat_days = base_event.repeat_days.split(',')
            for day_str in repeat_days:
                try:
                    day = int(day_str.strip())
                    new_start = base_event.start_time.replace(day=day)
                    new_end = base_event.end_time.replace(day=day)
                    if new_start < base_event.start_time:
                        new_start += timedelta(days=30)
                        new_end += timedelta(days=30)

                    Event.objects.create(
                        title=base_event.title,
                        description=base_event.description,
                        address=base_event.address,
                        table_size=base_event.table_size,
                        perks=base_event.perks,
                        start_time=new_start,
                        end_time=new_end,
                        is_repeating=False,
                        visibility=base_event.visibility,
                        created_by=user,
                        organization=organization,
                    )
                except Exception as e:
                    print("Error creating repeated event:", e)

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
