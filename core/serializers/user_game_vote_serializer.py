# core/serializers/user_game_vote_serializer.py

from rest_framework import serializers
from core.models import UserGameVote, Game

class GameSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'thumbnail_url']

class UserGameVoteSerializer(serializers.ModelSerializer):
    game = GameSimpleSerializer(read_only=True)

    class Meta:
        model = UserGameVote
        fields = ['id', 'user', 'event', 'game', 'rank', 'created_at']
