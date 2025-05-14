from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game, Organization, Event
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class FirstPlayerIsOrganizerTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="kurėjas", password="Slapta123!")
        self.user1 = User.objects.create_user(username="pirmas", password="Slapta123!")
        self.user2 = User.objects.create_user(username="antras", password="Slapta123!")

        self.org = Organization.objects.create(
            name="Test Klubas",
            description="FR-14 testas",
            privacy="public",
            created_by=self.owner,
            city="vilnius"
        )

        self.event = Event.objects.create(
            title="FR-14 renginys",
            description="Pirmas prisijungęs tampa organizatoriumi",
            address="Vilnius",
            organization=self.org,
            created_by=self.owner,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=3)),
            visibility="public",
            first_player_is_organizer=True
        )

    def login_and_get_token(self, username, password):
        response = self.client.post("/token/", {
            "username": username,
            "password": password
        }, format="json")
        self.assertEqual(response.status_code, 200)
        return response.data["access"]

    def test_first_player_becomes_organizer(self):
        token1 = self.login_and_get_token("pirmas", "Slapta123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")
        response1 = self.client.post(f"/events/{self.event.id}/join/")
        self.assertIn(response1.status_code, [200, 201])

        self.event.refresh_from_db()
        self.assertIn(self.user1, self.event.organizers.all())
        self.assertNotIn(self.user2, self.event.organizers.all())

    def test_second_player_does_not_become_organizer(self):
        # First user joins
        token1 = self.login_and_get_token("pirmas", "Slapta123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")
        self.client.post(f"/events/{self.event.id}/join/")

        # Second user joins
        token2 = self.login_and_get_token("antras", "Slapta123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")
        self.client.post(f"/events/{self.event.id}/join/")

        self.event.refresh_from_db()
        self.assertIn(self.user1, self.event.organizers.all())
        self.assertNotIn(self.user2, self.event.organizers.all())
