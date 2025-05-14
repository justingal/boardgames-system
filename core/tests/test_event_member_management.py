from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization, Event
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class EventMemberManagementTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="Labas123!")
        self.organizer = User.objects.create_user(username="organizer", password="Labas123!")
        self.participant = User.objects.create_user(username="player", password="Labas123!")

        self.org = Organization.objects.create(
            name="FR-16 Klubas",
            description="Narių valdymas",
            privacy="public",
            created_by=self.owner,
            city="vilnius"
        )

        self.event = Event.objects.create(
            title="Renginys",
            description="test",
            address="Kaunas",
            organization=self.org,
            created_by=self.owner,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=2)),
            visibility="public"
        )

        self.event.players.add(self.owner, self.organizer, self.participant)
        self.event.organizers.add(self.owner)

    def login(self, username):
        res = self.client.post("/token/", {"username": username, "password": "Labas123!"})
        self.assertEqual(res.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def test_owner_can_make_other_organizer(self):
        self.login("owner")
        response = self.client.post(f"/events/{self.event.id}/make-organizer/", {
            "user_id": self.organizer.id
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertIn(self.organizer, self.event.organizers.all())

    def test_owner_can_kick_player(self):
        self.login("owner")
        response = self.client.post(f"/events/{self.event.id}/kick-player/", {
            "user_id": self.participant.id
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertNotIn(self.participant, self.event.players.all())

    def test_player_cannot_kick_anyone(self):
        self.login("player")
        response = self.client.post(f"/events/{self.event.id}/kick-player/", {
            "user_id": self.owner.id
        }, format="json")
        self.assertEqual(response.status_code, 403)
