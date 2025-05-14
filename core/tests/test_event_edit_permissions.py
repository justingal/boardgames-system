from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization, Event
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class EventEditPermissionsTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="tikras", password="Slapta123!")
        self.auto_org = User.objects.create_user(username="auto", password="Slapta123!")

        self.org = Organization.objects.create(
            name="FR-15 Klubas",
            description="Organizavimo testas",
            privacy="public",
            created_by=self.owner,
            city="vilnius"
        )

        self.event = Event.objects.create(
            title="Senasis pavadinimas",
            description="Senas aprašas",
            address="Sena vieta",
            organization=self.org,
            created_by=self.owner,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=3)),
            visibility="private",
            first_player_is_organizer=True
        )

        self.event.players.add(self.auto_org)
        self.event.organizers.add(self.auto_org)  # automatinis
        self.event.players.add(self.owner)
        self.event.organizers.add(self.owner)     # tikrasis

    def get_token(self, username):
        response = self.client.post("/token/", {
            "username": username,
            "password": "Slapta123!"
        }, format="json")
        return response.data["access"]

    def test_true_organizer_can_edit_all_fields(self):
        token = self.get_token("tikras")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(f"/events/{self.event.id}/", {
            "title": "Naujas pavadinimas",
            "description": "Naujas aprašas",
            "address": "Nauja vieta",
            "table_size": "L",
            "start_time": make_aware(datetime.now() + timedelta(days=2)),
            "visibility": "public"
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Naujas pavadinimas")
        self.assertEqual(self.event.address, "Nauja vieta")

    def test_auto_organizer_can_edit_limited_fields(self):
        token = self.get_token("auto")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.patch(f"/events/{self.event.id}/", {
            "title": "Auto pavadinimas",
            "address": "Bandymas keisti adresą",
        }, format="json")

        self.event.refresh_from_db()

        # ✅ pavadinimas gali būti pakeistas
        self.assertEqual(self.event.title, "Auto pavadinimas")
        # ❌ adresas neturėtų pasikeisti
        self.assertNotEqual(self.event.address, "Bandymas keisti adresą")
