from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from core.models import UserProfile
from core.serializers import UserProfileFullSerializer


class UserFullProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Bandome gauti vartotojo profilį arba sukuriame naują, jei jo nėra
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'player'}  # Numatytoji rolė, jei profilis būtų sukurtas
        )

        serializer = UserProfileFullSerializer(profile, context={'request': request})
        return Response(serializer.data)