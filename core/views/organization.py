from rest_framework import viewsets, permissions
from core.models import Organization, GameCategory
from core.serializers.organization_serializer import OrganizationSerializer, GameCategorySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.models.organization import Organization, Membership
from rest_framework.generics import ListAPIView
from core.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
from core.models import Organization
from core.serializers import OrganizationSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, org_id, user_id):
    try:
        membership = Membership.objects.get(organization_id=org_id, user_id=user_id)
        if request.user != membership.organization.created_by:
            return Response({"error": "Only the organization leader can remove members."}, status=403)

        membership.delete()
        return Response({"detail": "Member removed."}, status=204)

    except Membership.DoesNotExist:
        return Response({"error": "Membership not found."}, status=404)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['privacy', 'categories', 'city']
    search_fields = ['name']

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)

        # Sukuriam Membership įrašą leaderiui
        Membership.objects.create(user=self.request.user, organization=org)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class GameCategoryViewSet(viewsets.ModelViewSet):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    permission_classes = [permissions.AllowAny]

class JoinOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)

        # Check if already a member
        if Membership.objects.filter(user=request.user, organization=organization).exists():
            return Response({"detail": "You are already a member."}, status=200)

        Membership.objects.create(user=request.user, organization=organization)
        return Response({"detail": f"You joined {organization.name}!"}, status=201)

class OrganizationMembersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs['pk']
        return User.objects.filter(
            id__in=Membership.objects.filter(organization_id=org_id).values_list('user_id', flat=True)
        )


