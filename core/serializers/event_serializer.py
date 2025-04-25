from rest_framework import serializers
from core.models import Event, Game
from django.contrib.auth.models import User
from core.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    games = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), many=True, required=False)
    is_participant = serializers.SerializerMethodField()
    first_player_is_organizer = serializers.BooleanField()
    # Replace actual_organizer with organizers
    organizers = UserSerializer(many=True, read_only=True)
    players = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'address', 'table_size', 'perks',
            'start_time', 'end_time', 'is_repeating', 'repeat_days',
            'visibility', 'created_by', 'organization', 'organization_name',
            'games', 'players', 'created_at', 'is_participant',
            'first_player_is_organizer', 'organizers'
        ]
        read_only_fields = [
            'players', 'created_by', 'organization',
            'organization_name', 'created_at', 'is_participant', 'organizers'
        ]

    def get_is_participant(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.players.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        games = validated_data.pop('games', [])
        event = Event.objects.create(**validated_data)

        # Add the creator as an organizer only if first_player_is_organizer is False
        if not validated_data.get('first_player_is_organizer', False):
            event.organizers.add(event.created_by)

        # Add games
        if games:
            event.games.set(games)

        return event