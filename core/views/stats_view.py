# core/views/stats_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.models import Organization, Event
from django.contrib.auth.models import User

class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "organizations": Organization.objects.count(),
            "events": Event.objects.count(),
            "users": User.objects.count()
        })
