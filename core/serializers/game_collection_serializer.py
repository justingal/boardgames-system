from rest_framework import serializers
from core.models.game_collection import GameCollection
from core.serializers.game_serializer import GameSerializer
from core.models.game import Game

class GameCollectionSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), source='game', write_only=True)

    class Meta:
        model = GameCollection
        fields = ['id', 'game', 'game_id', 'added_at']
