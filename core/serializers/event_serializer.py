
from rest_framework import serializers
from core.models import Event, Game
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    organization = serializers.PrimaryKeyRelatedField(read_only=True)
    games = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), many=True, required=False)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'address', 'table_size', 'perks',
            'start_time', 'end_time', 'is_repeating', 'repeat_days',
            'visibility', 'created_by', 'organization', 'games', 'players', 'created_at'
        ]
        read_only_fields = ['players', 'created_by', 'organization', 'created_at']
