from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization, Event
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class JoinEventTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="zaidejas", password="Labas123!")
        self.org = Organization.objects.create(
            name="Žaidimų klubas",
            description="Organizacijos aprašas",
            privacy="public",
            created_by=self.user,
            city="vilnius"
        )

        self.event = Event.objects.create(
            title="Testinis renginys",
            description="Bandomas renginys",
            address="Vilnius, Gedimino pr. 1",
            organization=self.org,
            created_by=self.user,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=3)),
            visibility="public"
        )

        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "zaidejas",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_join_event(self):
        response = self.client.post(f"/events/{self.event.id}/join/")
        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(self.event.players.filter(id=self.user.id).exists())
