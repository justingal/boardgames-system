from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game, UserGame

class CollectionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kolekcionierius", password="Labas123!")
        self.game1 = Game.objects.create(title="Catan", bgg_id=13)
        self.game2 = Game.objects.create(title="Carcassonne", bgg_id=822)

        UserGame.objects.create(user=self.user, game=self.game1)
        UserGame.objects.create(user=self.user, game=self.game2)

        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "kolekcionierius",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_can_view_user_collection(self):
        response = self.client.get("/collection/")
        print("🧪 Collection response:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)
        titles = [entry["game"]["title"] for entry in response.data]
        self.assertIn("Catan", titles)
        self.assertIn("Carcassonne", titles)
