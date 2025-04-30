# core/views/event_importable_games_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import GameCollection, EventAvailableGame

class EventImportableGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event_game_ids = EventAvailableGame.objects.filter(event_id=pk).values_list('game_id', flat=True)
        user_collection = GameCollection.objects.filter(user=request.user).exclude(game__id__in=event_game_ids)

        return Response([
            {
                "id": gc.id,
                "game": {
                    "id": gc.game.id,
                    "title": gc.game.title,
                    "thumbnail_url": gc.game.thumbnail_url,
                    "min_players": gc.game.min_players,
                    "max_players": gc.game.max_players,
                    "playtime_minutes": gc.game.playtime_minutes,
                }
            }
            for gc in user_collection
        ])
