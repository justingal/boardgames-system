from rest_framework import viewsets, permissions
from core.models import Event, Organization
from core.serializers import EventSerializer
from django.utils.dateparse import parse_datetime
from datetime import timedelta

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.all()
        perks = self.request.query_params.get('perks')

        if perks:
            perks_list = [p.strip() for p in perks.split(',')]
            for perk in perks_list:
                queryset = queryset.filter(perks__icontains=perk)

        # kiti filtrai ir grąžinimas
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile
        org_id = self.request.data.get("organization")

        # Check if user is member or organizer of selected organization
        try:
            organization = Organization.objects.get(id=org_id)
            if organization.created_by != user and user not in organization.members.all():
                raise PermissionError("User does not belong to this organization")
        except Organization.DoesNotExist:
            raise ValueError("Selected organization does not exist")

        base_event = serializer.save(created_by=user, organization=organization)

        # Create additional repeated events if applicable
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
