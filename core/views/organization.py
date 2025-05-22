from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Organization, Membership, GameCategory
from core.models.visibility import JoinRequest, Invite
from core.serializers.organization_serializer import OrganizationSerializer, GameCategorySerializer
from core.serializers import UserSerializer
from core.serializers.visibility_serializer import JoinRequestSerializer, InviteSerializer

from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
User = get_user_model()


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_member(request, org_id, user_id):
    try:
        membership = Membership.objects.get(organization_id=org_id, user_id=user_id)

        if request.user != membership.organization.created_by:
            return Response({"error": "Tik organizatorius gali šalinti narius."}, status=403)

        if request.user.id == user_id:
            return Response({"error": "Negalite pašalinti savęs."}, status=400)

        membership.delete()
        return Response({"detail": "Narys pašalintas."}, status=204)

    except Membership.DoesNotExist:
        return Response({"error": "Narys nerastas."}, status=404)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['privacy', 'category', 'city']
    search_fields = ['name']

    def perform_create(self, serializer):
        org = serializer.save(created_by=self.request.user)
        Membership.objects.create(user=self.request.user, organization=org)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.created_by != request.user:
            return Response({'detail': 'Neturite leidimo redaguoti šios organizacijos.'}, status=403)

        partial = kwargs.pop('partial', True)
        data = request.data.copy()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Organization.objects.none()

        try:
            if hasattr(user, 'profile') and getattr(user.profile, 'role', None) == 'organizer':
                return Organization.objects.filter(created_by=user)
            elif user.groups.filter(name='organizer').exists():
                return Organization.objects.filter(created_by=user)
        except Exception:
            pass

        return Organization.objects.all()

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        org = self.get_object()
        user = request.user

        if Membership.objects.filter(user=user, organization=org).exists():
            return Response({"detail": "Jau esate narys."}, status=200)

        if org.privacy == 'public':
            Membership.objects.create(user=user, organization=org)
            return Response({"detail": "Prisijungta prie organizacijos."})

        elif org.privacy == 'protected':
            JoinRequest.objects.get_or_create(user=user, organization=org)
            return Response({"detail": "Prašymas išsiųstas. Laukiama patvirtinimo."})

        elif org.privacy == 'private':
            return Response({"detail": "Privati organizacija. Reikalingas kvietimas."}, status=403)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def approve_request(self, request, pk=None):
        org = self.get_object()
        if org.created_by != request.user:
            return Response({"detail": "Tik organizatorius gali patvirtinti prašymus."}, status=403)

        req_id = request.data.get("request_id")
        join_request = get_object_or_404(JoinRequest, pk=req_id, organization=org)
        Membership.objects.create(user=join_request.user, organization=org)
        join_request.delete()
        return Response({"detail": "Prašymas patvirtintas."})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def invite(self, request, pk=None):
        org = self.get_object()
        if org.created_by != request.user:
            return Response({"detail": "Tik organizatorius gali siųsti kvietimus."}, status=403)

        user_id = request.data.get("user_id")
        invited_user = get_object_or_404(User, pk=user_id)
        Invite.objects.get_or_create(invited_user=invited_user, organization=org)
        return Response({"detail": "Kvietimas išsiųstas."})

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def accept_invite(self, request):
        invite_id = request.data.get("invite_id")
        invite = get_object_or_404(Invite, pk=invite_id, invited_user=request.user)

        if invite.is_accepted:
            return Response({"detail": "Kvietimas jau priimtas."})

        Membership.objects.create(user=request.user, organization=invite.organization)
        invite.is_accepted = True
        invite.save()
        return Response({"detail": "Prisijungta prie organizacijos."})

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def join_requests(self, request, pk=None):
        org = self.get_object()
        if org.created_by != request.user:
            return Response({"detail": "Tik organizatorius gali matyti prašymus."}, status=403)

        requests = JoinRequest.objects.filter(organization=org)
        serializer = JoinRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def invites(self, request):
        invites = Invite.objects.filter(invited_user=request.user, is_accepted=False)
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)


class GameCategoryViewSet(viewsets.ModelViewSet):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    permission_classes = [permissions.AllowAny]


class OrganizationMembersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs['pk']
        return User.objects.filter(
            id__in=Membership.objects.filter(organization_id=org_id).values_list('user_id', flat=True)
        )
