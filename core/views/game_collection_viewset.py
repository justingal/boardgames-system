# core/views.py
from rest_framework import viewsets, permissions
from core.models import GameCollection
from core.serializers import GameCollectionSerializer

class GameCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = GameCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GameCollection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
