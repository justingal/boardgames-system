from rest_framework import serializers
from core.models import EventAvailableGame
from core.serializers import GameSerializer

class EventAvailableGameSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    vote_count = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()  # <-- PRIDEDAM ČIA

    class Meta:
        model = EventAvailableGame
        fields = ['id', 'game', 'added_by', 'added_at', 'vote_count', 'rank', 'total_score']  # <-- ĮTRAUKTAS ČIA

    def get_vote_count(self, obj):
        return getattr(obj, 'vote_count', 0)

    def get_rank(self, obj):
        return getattr(obj, 'rank', None)

    def get_total_score(self, obj):
        return getattr(obj, 'total_score', None)
