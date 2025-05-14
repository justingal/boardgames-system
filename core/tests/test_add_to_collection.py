from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Game

class AddGameToCollectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kolekcija", password="Labas123!")
        self.login_and_get_token()

    def login_and_get_token(self):
        response = self.client.post("/token/", {
            "username": "kolekcija",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_add_game_by_bgg_id(self):
        response = self.client.post("/collections/add-from-search/", {
            "bgg_id": 123456,
            "title": "Test Game From BGG"
        }, format="json")

        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(Game.objects.filter(bgg_id=123456).exists())
        game = Game.objects.get(bgg_id=123456)
        self.assertIn(self.user, game.usercollection_set.first().users.all())
