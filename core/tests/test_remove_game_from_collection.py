from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game, GameCollection

class RemoveGameFromCollectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="salintojas", password="Labas123!")
        self.game = Game.objects.create(title="Bingo", bgg_id=777)
        GameCollection.objects.create(user=self.user, game=self.game)

        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "salintojas",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_remove_game_from_collection(self):
        response = self.client.delete(f"/collections/{self.game.id}/delete/")
        print("🔍 RESPONSE:", response.data)
        self.assertIn(response.status_code, [200, 204])
        self.assertFalse(GameCollection.objects.filter(user=self.user, game=self.game).exists())
