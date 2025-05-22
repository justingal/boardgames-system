from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime

from core.models import Event, Organization
from core.models.visibility import JoinRequest, Invite
from core.serializers import EventSerializer
from core.serializers.visibility_serializer import JoinRequestSerializer, InviteSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Event.objects.all()
        perks = self.request.query_params.get('perks')
        table_size = self.request.query_params.get('table_size')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        visibility = self.request.query_params.get('visibility')

        if perks:
            for perk in [p.strip() for p in perks.split(',')]:
                queryset = queryset.filter(perks__icontains=perk)

        if table_size:
            queryset = queryset.filter(table_size=table_size)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if start_date:
            queryset = queryset.filter(start_time__date=start_date)

        if visibility:
            queryset = queryset.filter(visibility=visibility)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        org_id = self.request.data.get("organization")

        organization = get_object_or_404(Organization, id=org_id)
        if organization.created_by != user and user not in organization.members.all():
            raise PermissionDenied("Naudotojas nepriklauso organizacijai.")

        base_event = serializer.save(created_by=user, organization=organization)

        if not base_event.first_player_is_organizer:
            base_event.players.add(user)
            base_event.organizers.add(user)
            base_event.save()

        if base_event.is_repeating and base_event.repeat_days:
            self._create_repeating_events(base_event, organization, user)

    def _create_repeating_events(self, base_event, organization, user):
        repeat_dates = base_event.repeat_days.split(',')
        base_start_time = base_event.start_time.time()
        base_end_time = base_event.end_time.time()

        for date_str in repeat_dates:
            date_str = date_str.strip()
            if not date_str or date_str == base_event.start_time.date().isoformat():
                continue

            try:
                date_obj = datetime.fromisoformat(date_str).date()
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                except Exception:
                    continue

            naive_start = datetime.combine(date_obj, base_start_time)
            naive_end = datetime.combine(date_obj, base_end_time)
            if naive_end < naive_start:
                naive_end += timedelta(days=1)

            start_time = timezone.make_aware(naive_start) if timezone.is_aware(base_event.start_time) else naive_start
            end_time = timezone.make_aware(naive_end) if timezone.is_aware(base_event.end_time) else naive_end

            repeated_event = Event.objects.create(
                title=base_event.title,
                description=base_event.description,
                address=base_event.address,
                table_size=base_event.table_size,
                perks=base_event.perks,
                start_time=start_time,
                end_time=end_time,
                is_repeating=False,
                visibility=base_event.visibility,
                created_by=user,
                organization=organization,
                first_player_is_organizer=base_event.first_player_is_organizer,
            )

            if not base_event.first_player_is_organizer:
                repeated_event.players.add(user)
                repeated_event.organizers.add(user)
                repeated_event.save()

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organization.created_by != request.user:
            return Response({'detail': 'Neturite teisės ištrinti šio renginio.'},
                            status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        is_creator = event.created_by == user
        is_organizer = event.organizers.filter(id=user.id).exists()

        if not (is_creator or is_organizer):
            raise PermissionDenied("Tik renginio kūrėjas arba organizatoriai gali redaguoti renginį.")

        mutable_data = request.data.copy()
        mutable_data.pop('players', None)
        mutable_data.pop('organizers', None)

        if is_organizer and not is_creator and event.first_player_is_organizer:
            allowed_fields = ['title', 'description', 'visibility']
            for key in list(mutable_data.keys()):
                if key not in allowed_fields:
                    mutable_data.pop(key)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(event, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # --- JOIN / REQUEST / INVITE LOGIKA ŽEMIAU ---

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if event.players.filter(id=user.id).exists():
            return Response({'detail': 'Jau esate prisijungęs prie šio renginio.'}, status=400)

        if event.visibility == 'public':
            event.players.add(user)
            return Response({'detail': 'Prisijungta sėkmingai.'})

        elif event.visibility == 'protected':
            JoinRequest.objects.get_or_create(user=user, event=event)
            return Response({'detail': 'Prašymas išsiųstas. Laukiama patvirtinimo.'})

        elif event.visibility == 'private':
            return Response({'detail': 'Privatus renginys. Reikia kvietimo.'}, status=403)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve_request(self, request, pk=None):
        event = self.get_object()
        if event.organization.created_by != request.user:
            return Response({'detail': 'Tik organizatorius gali patvirtinti.'}, status=403)

        req_id = request.data.get("request_id")
        join_request = get_object_or_404(JoinRequest, pk=req_id, event=event)
        event.players.add(join_request.user)
        join_request.delete()
        return Response({"detail": "Prašymas patvirtintas."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def invite(self, request, pk=None):
        event = self.get_object()
        if event.organization.created_by != request.user:
            return Response({"detail": "Tik organizatorius gali siųsti kvietimus."}, status=403)

        user_id = request.data.get("user_id")
        invited_user = get_object_or_404(User, pk=user_id)
        Invite.objects.get_or_create(invited_user=invited_user, event=event)
        return Response({"detail": "Kvietimas išsiųstas."})

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def accept_invite(self, request):
        invite_id = request.data.get("invite_id")
        invite = get_object_or_404(Invite, pk=invite_id, invited_user=request.user)

        if invite.is_accepted:
            return Response({"detail": "Kvietimas jau priimtas."})

        invite.event.players.add(request.user)
        invite.is_accepted = True
        invite.save()
        return Response({"detail": "Prisijungta prie renginio."})

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def join_requests(self, request, pk=None):
        event = self.get_object()
        if event.organization.created_by != request.user:
            return Response({"detail": "Tik organizatorius gali matyti prašymus."}, status=403)

        requests = JoinRequest.objects.filter(event=event)
        serializer = JoinRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def invites(self, request):
        invites = Invite.objects.filter(invited_user=request.user, is_accepted=False)
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)
