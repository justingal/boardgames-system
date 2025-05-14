from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game, Organization, Event, UserGameVote
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class EventVoteResultsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="balsuotojas", password="Labas123!")
        self.org = Organization.objects.create(
            name="Rezultatų klubas",
            description="test",
            privacy="public",
            created_by=self.user,
            city="vilnius"
        )
        self.game1 = Game.objects.create(title="Catan", bgg_id=13)
        self.game2 = Game.objects.create(title="7 Wonders", bgg_id=68448)
        self.event = Event.objects.create(
            title="Renginys su balsais",
            description="test",
            address="Kaunas",
            organization=self.org,
            created_by=self.user,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=2)),
            visibility="public"
        )
        self.event.players.add(self.user)

        # Sukuriam balsus rankomis
        UserGameVote.objects.create(event=self.event, user=self.user, game=self.game1, rank=1)
        UserGameVote.objects.create(event=self.event, user=self.user, game=self.game2, rank=2)

        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "balsuotojas",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_vote_results_visible(self):
        response = self.client.get(f"/events/{self.event.id}/vote-results/")
        print("📊 Vote results response:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        titles = [item["game__title"] for item in response.data]
        self.assertIn("Catan", titles)
        self.assertIn("7 Wonders", titles)
