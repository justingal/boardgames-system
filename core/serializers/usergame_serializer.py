from rest_framework import serializers
from core.models import UserGame
from .game_serializer import GameSerializer

class UserGameSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = UserGame
        fields = ['id', 'game', 'date_added']
