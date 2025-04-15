# core/views/event_viewset.py

from rest_framework import viewsets, permissions
from core.models import Event
from core.serializers.event_serializer import EventSerializer
from rest_framework.exceptions import PermissionDenied

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        profile = user.profile

        if profile.role != 'organizer':
            raise PermissionDenied("Tik organizatoriai gali kurti renginius.")

        if not profile.organization:
            raise PermissionDenied("Neturite priskirtos organizacijos.")

        serializer.save(created_by=user, organization=profile.organization)
