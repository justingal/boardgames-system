from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from core.serializers import RegisterSerializer
from core.serializers.organizer_serializer import OrganizerRegisterSerializer

from rest_framework import generics, permissions
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from core.tokens import get_tokens_for_user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class OrganizerRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizerRegisterSerializer
    permission_classes = [permissions.AllowAny]


