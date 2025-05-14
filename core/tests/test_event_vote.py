from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization, Event, Game
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class EventVoteTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="balsuotojas", password="Labas123!")
        self.org = Organization.objects.create(
            name="Balsavimo klubas",
            description="Aprašas",
            privacy="public",
            created_by=self.user,
            city="vilnius"
        )
        self.game = Game.objects.create(title="Carcassonne", bgg_id=999)
        self.event = Event.objects.create(
            title="Renginys su balsavimu",
            description="Bandom balsuoti",
            address="Vilnius",
            organization=self.org,
            created_by=self.user,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=2)),
            visibility="public"
        )
        self.event.games.add(self.game)
        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "balsuotojas",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_vote_for_game(self):
        def test_vote_for_game(self):
            response = self.client.post(f"/events/{self.event.id}/vote/", {
                "votes": [self.game.id]  # ✅ pataisytas laukas
            }, format="json")

            print("✅ RESPONSE:", response.data)

            self.assertIn(response.status_code, [200, 201])
            self.assertIn("success", str(response.data).lower())


