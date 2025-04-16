from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Organization
from core.serializers import OrganizationSerializer

class UserOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orgs = Organization.objects.filter(members=user)
        serializer = OrganizationSerializer(orgs, many=True)
        return Response(serializer.data)
