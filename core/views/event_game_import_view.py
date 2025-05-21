# core/views/event_game_import_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from core.models import Event, GameCollection, Game, EventAvailableGame
from core.serializers import EventAvailableGameSerializer
from core.models import EventAvailableGame, UserGameVote
from django.db.models import Sum, Count, F


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
            return Response({"error": "Renginys nerastas."}, status=404)

        all_games = EventAvailableGame.objects.filter(event=event).select_related('game')

        vote_data = (
            UserGameVote.objects
            .filter(event=event)
            .values('game')
            .annotate(
                total_score=Sum('rank'),       # mažiau = geriau
                vote_count=Count('id')
            )
            .order_by('total_score')
        )

        rank_map = {}
        vote_count_map = {}
        total_score_map = {}

        for index, v in enumerate(vote_data):
            game_id = v['game']
            rank_map[game_id] = index + 1
            vote_count_map[game_id] = v['vote_count']
            total_score_map[game_id] = v['total_score']

        # Priskiriame į objektus
        for g in all_games:
            g.rank = rank_map.get(g.game.id)
            g.vote_count = vote_count_map.get(g.game.id, 0)
            g.total_score = total_score_map.get(g.game.id)  # <- naujas laukas frontendui

        # Rikiavimas pagal rank (mažiau yra geriau)
        ordered_games = sorted(all_games, key=lambda g: g.rank if g.rank is not None else 9999)

        serializer = EventAvailableGameSerializer(ordered_games, many=True)
        return Response(serializer.data)
