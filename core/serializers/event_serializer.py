from rest_framework import serializers
from core.models import Event, Game
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    games = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), many=True, required=False)
    is_participant = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'address', 'table_size', 'perks',
            'start_time', 'end_time', 'is_repeating', 'repeat_days',
            'visibility', 'created_by', 'organization', 'organization_name',
            'games', 'players', 'created_at', 'is_participant'
        ]
        read_only_fields = [
            'players', 'created_by', 'organization',
            'organization_name', 'created_at', 'is_participant'
        ]

    def get_is_participant(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.players.filter(id=request.user.id).exists()
        return False
