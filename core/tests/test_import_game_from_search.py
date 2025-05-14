from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import GameCollection

class AddGameFromSearchTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="searcher", password="Labas123!")
        self.login()

    def login(self):
        response = self.client.post("/token/", {
            "username": "searcher",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_add_game_by_bgg_id(self):
        # Pvz. BGG ID: 13 = Catan
        response = self.client.post("/collections/add-from-search/", {
            "bgg_id": 13
        }, format="json")

        print("🔍 RESPONSE:", response.data)
        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(GameCollection.objects.filter(user=self.user, game__bgg_id=13).exists())
