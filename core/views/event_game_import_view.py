# core/views/event_game_import_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from core.models import Event, GameCollection, Game, EventAvailableGame
from core.serializers import EventAvailableGameSerializer

class EventGameImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        if not (event.players.filter(id=request.user.id).exists() or event.created_by == request.user):
            return Response({"error": "Tik renginio dalyviai gali importuoti žaidimus."}, status=status.HTTP_403_FORBIDDEN)

        game_ids = request.data.get('game_ids')
        if not game_ids:
            return Response({"error": "Nepateikti žaidimų ID."}, status=status.HTTP_400_BAD_REQUEST)

        imported_count = 0
        for game_id in game_ids:
            try:
                game = Game.objects.get(id=game_id)
                _, created = EventAvailableGame.objects.get_or_create(event=event, game=game, added_by=request.user)
                if created:
                    imported_count += 1
            except Game.DoesNotExist:
                continue

        return Response({"message": f"{imported_count} žaidimai sėkmingai importuoti į renginį."}, status=status.HTTP_201_CREATED)


class EventAvailableGameListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is allowed to view
        if not (event.players.filter(id=request.user.id).exists() or event.created_by == request.user):
            return Response({"error": "Tik renginio dalyviai gali matyti galimus žaidimus."}, status=status.HTTP_403_FORBIDDEN)

        queryset = EventAvailableGame.objects.filter(event=event)
        serializer = EventAvailableGameSerializer(queryset, many=True)
        return Response(serializer.data)
