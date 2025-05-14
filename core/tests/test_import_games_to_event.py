from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game, Organization, Event, EventAvailableGame
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class ImportGamesToEventTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="organizatorius", password="Labas123!")
        self.org = Organization.objects.create(
            name="Importavimo klubas",
            description="Import test",
            privacy="public",
            created_by=self.user,
            city="vilnius"
        )
        self.game1 = Game.objects.create(title="Catan", bgg_id=13)
        self.game2 = Game.objects.create(title="7 Wonders", bgg_id=68448)
        self.event = Event.objects.create(
            title="Importo renginys",
            description="Bandymas",
            address="Vilnius",
            organization=self.org,
            created_by=self.user,
            table_size="M",
            start_time=make_aware(datetime.now() + timedelta(days=1)),
            end_time=make_aware(datetime.now() + timedelta(days=1, hours=2)),
            visibility="public"
        )
        self.event.players.add(self.user)  # 👈 svarbu, nes kitaip 403

        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "organizatorius",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_import_games_to_event(self):
        response = self.client.post(f"/events/{self.event.id}/import-games/", {
            "game_ids": [self.game1.id, self.game2.id]
        }, format="json")

        print("🧪 RESPONSE:", response.data)
        self.assertEqual(response.status_code, 201)

        self.assertTrue(EventAvailableGame.objects.filter(event=self.event, game=self.game1).exists())
        self.assertTrue(EventAvailableGame.objects.filter(event=self.event, game=self.game2).exists())
