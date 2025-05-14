from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game

class ImportGameByBGGIDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="importuotojas", password="Labas123!")
        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "importuotojas",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_import_game_by_bgg_id(self):
        response = self.client.post("/collections/import-bgg-id/", {
            "bgg_id": 13,  # Catan
            "title": "Catan"
        }, format="json")
        print("💥 RESPONSE DATA:", response.data)
        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(Game.objects.filter(bgg_id=13).exists())
