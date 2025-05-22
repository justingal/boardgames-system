from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(
            Q(email__icontains=query) | Q(username__icontains=query)
        )[:10]

        results = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
        return Response(results)
