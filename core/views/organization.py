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

        # Tik organizatorius gali šalinti
        if request.user != membership.organization.created_by:
            return Response({"error": "Only the organization leader can remove members."}, status=403)

        # Negalima pašalinti savęs
        if request.user.id == user_id:
            return Response({"error": "Negalite pašalinti savęs."}, status=400)

        membership.delete()
        return Response({"detail": "Member removed."}, status=204)

    except Membership.DoesNotExist:
        return Response({"error": "Membership not found."}, status=404)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['privacy', 'categories', 'city']
    search_fields = ['name']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Tik organizatorius gali redaguoti
        if instance.created_by != request.user:
            return Response({'detail': 'Neturite leidimo redaguoti šios organizacijos.'}, status=403)

        partial = kwargs.pop('partial', True)  # PATCH by default
        data = request.data.copy()

        # Apdorojam kategoriją
        category_name = data.pop('category_name', None)
        if category_name:
            category, _ = GameCategory.objects.get_or_create(name=category_name)
            instance.categories.set([category])

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)

        # Sukuriam Membership įrašą leaderiui
        Membership.objects.create(user=self.request.user, organization=org)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        user = self.request.user

        # Jei vartotojas nėra prisijungęs, grąžink tuščią queryset
        if not user.is_authenticated:
            return Organization.objects.none()

        # Jei vartotojas yra organizatorius, grąžink tik jo sukurtas organizacijas
        # Tikriname ar vartotojas turi profilio modelį su role arba naudojame groups
        try:
            # Bandome gauti rolę iš profilio, jei toks yra
            if hasattr(user, 'profile') and hasattr(user.profile, 'role') and user.profile.role == 'organizer':
                return Organization.objects.filter(created_by=user)
            # Arba tikriname ar vartotojas priklauso organizatorių grupei
            elif user.groups.filter(name='organizer').exists():
                return Organization.objects.filter(created_by=user)
        except Exception:
            # Jei nepavyksta patikrinti rolės, grąžiname visas organizacijas
            pass

        # Kitų tipų vartotojams grąžink visas organizacijas
        return Organization.objects.all()

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


