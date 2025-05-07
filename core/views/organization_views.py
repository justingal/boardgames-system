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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:
            return Response({'error': 'Tik kūrėjas gali ištrinti.'}, status=403)
        self.perform_destroy(instance)
        return Response(status=204)
