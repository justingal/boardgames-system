# core/views/event_vote_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from core.models import Event, Game, UserGameVote

class EventGameVoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """ Vartotojas pateikia savo balsus už žaidimus """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        if not (event.players.filter(id=request.user.id).exists() or event.created_by == request.user):
            return Response({"error": "Tik renginio dalyviai gali balsuoti."}, status=status.HTTP_403_FORBIDDEN)

        votes = request.data.get('votes')  # Pvz.: [{'game_id': 4, 'rank': 1}, {'game_id': 2, 'rank': 2}]
        if not votes:
            return Response({"error": "Nepateikti balsai."}, status=status.HTTP_400_BAD_REQUEST)

        # Ištrinti senus balsus
        UserGameVote.objects.filter(event=event, user=request.user).delete()

        # Išsaugoti naujus balsus
        for vote in votes:
            game_id = vote.get('game_id')
            rank = vote.get('rank')
            try:
                game = Game.objects.get(id=game_id)
                UserGameVote.objects.create(event=event, user=request.user, game=game, rank=rank)
            except Game.DoesNotExist:
                continue  # Praleidžiam, jei žaidimo nėra

        return Response({"message": "Balsai sėkmingai išsaugoti."}, status=status.HTTP_201_CREATED)


class EventGameVoteResultsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        """ Gauti balsavimo rezultatus """
        from django.db.models import Sum, Count

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        results = (
            UserGameVote.objects
            .filter(event=event)
            .values('game__id', 'game__title')
            .annotate(total_score=Sum('rank'), votes_count=Count('id'))
            .order_by('total_score')  # Mažesnis rank = aukštesnė vieta
        )

        return Response(results)
