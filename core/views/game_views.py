from rest_framework import generics, permissions
from core.models import Game
from core.serializers import GameSerializer

class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
