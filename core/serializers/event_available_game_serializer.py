# core/serializers/event_available_game_serializer.py
from rest_framework import serializers
from core.models import EventAvailableGame
from core.serializers import GameSerializer

class EventAvailableGameSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = EventAvailableGame
        fields = ['id', 'game', 'added_by', 'added_at']
