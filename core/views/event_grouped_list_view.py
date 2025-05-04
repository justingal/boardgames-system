from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.timezone import now
from core.models import Event
from core.serializers import EventSerializer
from datetime import timedelta, datetime
from django.db.models import Q


class GroupedEventsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, org_id=None):
        today = now().date()
        user = request.user

        # Filtrai iš query params
        search = request.query_params.get('search')
        table_size = request.query_params.get('table_size')
        visibility = request.query_params.get('visibility')
        perks = request.query_params.get('perks')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        is_participant = request.query_params.get('is_participant') == 'true'

        # Naujas filtras - konkreti data
        start_date = request.query_params.get('start_date')

        def apply_common_filters(queryset):
            if search:
                queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
            if table_size:
                queryset = queryset.filter(table_size=table_size)
            if visibility:
                queryset = queryset.filter(visibility=visibility)
            if perks:
                for perk in perks.split(','):
                    queryset = queryset.filter(perks__icontains=perk)
            if is_participant and user.is_authenticated:
                queryset = queryset.filter(players=user)
            if not user.is_authenticated:
                queryset = queryset.filter(visibility='public')
            return queryset

        def apply_date_filters(queryset):
            # Jei yra konkretus datos filtras, naudojame jį
            if start_date:
                try:
                    # Bandome konvertuoti į datą
                    date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                    return queryset.filter(start_time__date=date_obj)
                except (ValueError, TypeError):
                    pass
            # Jei nėra konkrečios datos, bet yra metai ir mėnuo
            elif year and month:
                try:
                    return queryset.filter(
                        start_time__year=int(year),
                        start_time__month=int(month)
                    )
                except ValueError:
                    pass
            return queryset

        # Pasirenkam organizacijos filtrą (jei yra)
        base_query = Event.objects.all()
        if org_id:
            base_query = base_query.filter(organization_id=org_id)

        # Grupės
        events_today = base_query.filter(start_time__date=today)
        events_upcoming = base_query.filter(start_time__date__gt=today)
        events_past = base_query.filter(end_time__lt=now())

        # Pritaikome filtrus kiekvienai grupei atskirai
        events_today = apply_common_filters(events_today)
        events_today = apply_date_filters(events_today).order_by('start_time')

        events_upcoming = apply_common_filters(events_upcoming)
        events_upcoming = apply_date_filters(events_upcoming).order_by('start_time')

        events_past = apply_common_filters(events_past)
        events_past = apply_date_filters(events_past).order_by('-end_time')

        # Serializacija
        serializer_context = {'request': request}
        return Response({
            'today': EventSerializer(events_today, many=True, context=serializer_context).data,
            'upcoming': EventSerializer(events_upcoming, many=True, context=serializer_context).data,
            'past': EventSerializer(events_past, many=True, context=serializer_context).data,
        })