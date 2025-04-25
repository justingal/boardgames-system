from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Event
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied


class MakeOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        # Check if current user is an organizer
        is_organizer = event.organizers.filter(id=request.user.id).exists() or event.created_by == request.user

        if not is_organizer:
            raise PermissionDenied("Tik organizatorius gali suteikti organizatoriaus teises.")

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "Nenurodytas vartotojo ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_organizer = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Vartotojas nerastas."}, status=status.HTTP_404_NOT_FOUND)

        if not event.players.filter(id=new_organizer.id).exists():
            return Response({"error": "Šis vartotojas nėra prisijungęs prie renginio."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add the user to organizers
        event.organizers.add(new_organizer)

        return Response({"message": f"✅ Organizatoriaus teisės suteiktos: {new_organizer.username}"},
                        status=status.HTTP_200_OK)


class KickPlayerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        # Check if current user is an organizer
        is_organizer = event.organizers.filter(id=request.user.id).exists() or event.created_by == request.user

        if not is_organizer:
            raise PermissionDenied("Tik organizatorius gali išmesti žaidėjus.")

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "Nenurodytas vartotojo ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            player_to_remove = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Vartotojas nerastas."}, status=status.HTTP_404_NOT_FOUND)

        if not event.players.filter(id=player_to_remove.id).exists():
            return Response({"error": "Šis vartotojas nėra prisijungęs prie renginio."}, status=status.HTTP_400_BAD_REQUEST)

        # Don't allow removing other organizers
        if event.organizers.filter(id=player_to_remove.id).exists():
            # Add option to remove organizer status but keep as player
            if request.data.get('remove_organizer_only'):
                event.organizers.remove(player_to_remove)
                return Response({"message": f"Vartotojui {player_to_remove.username} pašalintos organizatoriaus teisės."}, status=status.HTTP_200_OK)
            return Response({"error": "Negalite išmesti organizatoriaus. Pirmiau pašalinkite organizatoriaus teises."}, status=status.HTTP_400_BAD_REQUEST)

        event.players.remove(player_to_remove)
        return Response({"message": f"Vartotojas {player_to_remove.username} sėkmingai išmestas."}, status=status.HTTP_200_OK)

class RemoveOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Renginys nerastas."}, status=status.HTTP_404_NOT_FOUND)

        # Only organizers can remove other organizers
        is_organizer = event.organizers.filter(id=request.user.id).exists() or event.created_by == request.user

        if not is_organizer:
            raise PermissionDenied("Tik organizatorius gali pašalinti organizatoriaus teises.")

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "Nenurodytas vartotojo ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            organizer_to_remove = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Vartotojas nerastas."}, status=status.HTTP_404_NOT_FOUND)

        if not event.organizers.filter(id=organizer_to_remove.id).exists():
            return Response({"error": "Šis vartotojas nėra organizatorius."}, status=status.HTTP_400_BAD_REQUEST)

        # Don't allow removing yourself if you're the created_by user
        if organizer_to_remove == request.user and event.created_by == request.user:
            return Response({"error": "Renginio kūrėjas negali pašalinti savo organizatoriaus teisių."}, status=status.HTTP_400_BAD_REQUEST)

        event.organizers.remove(organizer_to_remove)
        return Response({"message": f"Organizatoriaus teisės pašalintos: {organizer_to_remove.username}"}, status=status.HTTP_200_OK)