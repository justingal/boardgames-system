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

    def _is_event_organizer(self, event, user):
        """Helper method to check if user is an event organizer"""
        return (event.created_by == user or
                user in event.organizers.all() or
                event.organization.created_by == user)

    # --- JOIN / LEAVE / REQUEST / INVITE LOGIKA ---

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if already a participant
        if event.players.filter(id=user.id).exists():
            return Response({'detail': 'Jau esate prisijungęs prie šio renginio.'}, status=400)

        # Handle different visibility levels
        if event.visibility == 'public':
            event.players.add(user)

            # Special logic for first_player_is_organizer events
            if event.first_player_is_organizer and event.players.count() == 1:
                event.organizers.add(user)
                return Response({'detail': 'Prisijungta sėkmingai kaip organizatorius!'}, status=200)

            return Response({'detail': 'Prisijungta sėkmingai.'}, status=200)

        elif event.visibility == 'protected':
            # Create join request for protected events
            join_request, created = JoinRequest.objects.get_or_create(user=user, event=event)
            if created:
                return Response({'detail': 'Prašymas išsiųstas. Laukiama patvirtinimo.'}, status=201)
            else:
                return Response({'detail': 'Prašymas jau išsiųstas. Laukiama patvirtinimo.'}, status=200)

        elif event.visibility == 'private':
            return Response({'detail': 'Privatus renginys. Reikia kvietimo.'}, status=403)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user is a participant
        if not event.players.filter(id=user.id).exists():
            return Response({'detail': 'Nesate šio renginio dalyvis.'}, status=400)

        # Don't allow event creator to leave if they're the only organizer
        if (event.created_by == user and
                event.organizers.count() == 1 and
                event.organizers.filter(id=user.id).exists()):
            return Response({
                'detail': 'Negalite išeiti iš renginio būdami vieninteliu organizatoriumi.'
            }, status=400)

        # Remove from players and organizers
        event.players.remove(user)
        if event.organizers.filter(id=user.id).exists():
            event.organizers.remove(user)

        return Response({'detail': 'Sėkmingai išėjote iš renginio.'}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve_request(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can approve requests (organizers or org creator)
        if not self._is_event_organizer(event, user):
            return Response({'detail': 'Tik organizatoriai gali patvirtinti prašymus.'}, status=403)

        req_id = request.data.get("request_id")
        if not req_id:
            return Response({'detail': 'Trūksta request_id parametro.'}, status=400)

        join_request = get_object_or_404(JoinRequest, pk=req_id, event=event)

        # Add user to event
        event.players.add(join_request.user)

        # Special logic for first_player_is_organizer events
        if event.first_player_is_organizer and event.players.count() == 1:
            event.organizers.add(join_request.user)

        # Delete the request
        join_request.delete()

        return Response({"detail": "Prašymas patvirtintas."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject_request(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can reject requests (organizers or org creator)
        if not self._is_event_organizer(event, user):
            return Response({'detail': 'Tik organizatoriai gali atmesti prašymus.'}, status=403)

        req_id = request.data.get("request_id")
        if not req_id:
            return Response({'detail': 'Trūksta request_id parametro.'}, status=400)

        join_request = get_object_or_404(JoinRequest, pk=req_id, event=event)
        join_request.delete()

        return Response({"detail": "Prašymas atmestas."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def invite(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can send invites (organizers or org creator)
        if not self._is_event_organizer(event, user):
            return Response({"detail": "Tik organizatoriai gali siųsti kvietimus."}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "Trūksta user_id parametro."}, status=400)

        invited_user = get_object_or_404(User, pk=user_id)

        # Check if user is already a participant
        if event.players.filter(id=invited_user.id).exists():
            return Response({"detail": "Naudotojas jau yra renginio dalyvis."}, status=400)

        # Create or get existing invite
        invite, created = Invite.objects.get_or_create(
            invited_user=invited_user,
            event=event,
            defaults={'is_accepted': False}
        )

        if created:
            return Response({"detail": "Kvietimas išsiųstas."})
        else:
            return Response({"detail": "Kvietimas jau buvo išsiųstas."})

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def accept_invite(self, request):
        invite_id = request.data.get("invite_id")
        if not invite_id:
            return Response({"detail": "Trūksta invite_id parametro."}, status=400)

        invite = get_object_or_404(Invite, pk=invite_id, invited_user=request.user)

        if invite.is_accepted:
            return Response({"detail": "Kvietimas jau priimtas."})

        # Add user to event
        invite.event.players.add(request.user)

        # Special logic for first_player_is_organizer events
        if (invite.event.first_player_is_organizer and
                invite.event.players.count() == 1):
            invite.event.organizers.add(request.user)

        # Mark invite as accepted
        invite.is_accepted = True
        invite.save()

        return Response({"detail": "Prisijungta prie renginio."})

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def join_requests(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can view requests (organizers or org creator)
        if not self._is_event_organizer(event, user):
            return Response({"detail": "Tik organizatoriai gali matyti prašymus."}, status=403)

        requests = JoinRequest.objects.filter(event=event)
        serializer = JoinRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def invites(self, request):
        invites = Invite.objects.filter(invited_user=request.user, is_accepted=False)
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)

    # --- ORGANIZER MANAGEMENT ---

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def make_organizer(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can manage organizers
        if not self._is_event_organizer(event, user):
            return Response({'detail': 'Tik organizatoriai gali suteikti organizatoriaus teises.'}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "Trūksta user_id parametro."}, status=400)

        target_user = get_object_or_404(User, pk=user_id)

        # Check if target user is a participant
        if not event.players.filter(id=target_user.id).exists():
            return Response({"detail": "Naudotojas nėra renginio dalyvis."}, status=400)

        # Check if already an organizer
        if event.organizers.filter(id=target_user.id).exists():
            return Response({"detail": "Naudotojas jau yra organizatorius."}, status=400)

        # Add as organizer
        event.organizers.add(target_user)

        return Response({"message": "Organizatoriaus teisės suteiktos."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_organizer(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can manage organizers
        if not self._is_event_organizer(event, user):
            return Response({'detail': 'Tik organizatoriai gali šalinti organizatoriaus teises.'}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "Trūksta user_id parametro."}, status=400)

        target_user = get_object_or_404(User, pk=user_id)

        # Don't allow removing creator if they're the only organizer
        if (target_user == event.created_by and event.organizers.count() == 1):
            return Response({
                "detail": "Negalima pašalinti renginio kūrėjo teisių, jei jis yra vienintelis organizatorius."
            }, status=400)

        # Remove organizer status
        if event.organizers.filter(id=target_user.id).exists():
            event.organizers.remove(target_user)
            return Response({"message": "Organizatoriaus teisės pašalintos."})
        else:
            return Response({"detail": "Naudotojas nėra organizatorius."}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def kick_player(self, request, pk=None):
        event = self.get_object()
        user = request.user

        # Check if user can kick players
        if not self._is_event_organizer(event, user):
            return Response({'detail': 'Tik organizatoriai gali išmesti dalyvius.'}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "Trūksta user_id parametro."}, status=400)

        target_user = get_object_or_404(User, pk=user_id)

        # Don't allow kicking organizers
        if event.organizers.filter(id=target_user.id).exists():
            return Response({"detail": "Negalima išmesti organizatorių."}, status=400)

        # Check if target user is a participant
        if not event.players.filter(id=target_user.id).exists():
            return Response({"detail": "Naudotojas nėra renginio dalyvis."}, status=400)

        # Remove from event
        event.players.remove(target_user)

        return Response({"message": "Žaidėjas išmestas iš renginio."})