from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models.game_collection import GameCollection
from core.views.game_collection_csv_import import fetch_game_from_bgg


class AddGameFromSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Request data:", request.data)  # <-- pridėk

        bgg_id = request.data.get("bgg_id")
        if not bgg_id:
            return Response({"error": "bgg_id is required"}, status=400)

        game = fetch_game_from_bgg(bgg_id=int(bgg_id))
        if not game:
            return Response({"error": "Nepavyko atsisiųsti žaidimo."}, status=400)

        if GameCollection.objects.filter(user=request.user, game=game).exists():
            return Response({"message": "Žaidimas jau yra kolekcijoje."}, status=200)

        GameCollection.objects.create(user=request.user, game=game)
        return Response({"message": f"✅ Pridėtas: {game.title}"}, status=201)
