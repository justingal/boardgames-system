from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Game, UserGame
from core.serializers import UserGameSerializer

class UserCollectionView(generics.ListAPIView):
    serializer_class = UserGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserGame.objects.filter(user=self.request.user)

class AddToCollectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        game_id = request.data.get('game_id')
        try:
            game = Game.objects.get(id=game_id)
            user_game, created = UserGame.objects.get_or_create(user=request.user, game=game)
            if not created:
                return Response({'detail': 'Game already in collection.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Game added to collection.'}, status=status.HTTP_201_CREATED)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)
