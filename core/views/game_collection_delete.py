from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models.game_collection import GameCollection

class RemoveGameFromCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, game_id):
        try:
            collection_item = GameCollection.objects.get(user=request.user, game__id=game_id)
            collection_item.delete()
            return Response({"message": "Žaidimas pašalintas."}, status=status.HTTP_200_OK)
        except GameCollection.DoesNotExist:
            return Response({"error": "Žaidimas nerastas kolekcijoje."}, status=status.HTTP_404_NOT_FOUND)
