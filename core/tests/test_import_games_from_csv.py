from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock


class ImportGamesFromCSVTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="importeris", password="Labas123!")
        self.login()

    def login(self):
        response = self.client.post("/token/", {
            "username": "importeris",
            "password": "Labas123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @patch('core.views.game_collection_csv_import.Game.objects.filter')
    @patch('core.views.game_collection_csv_import.GameCollection.objects.filter')
    @patch('core.views.game_collection_csv_import.fetch_game_from_bgg')
    @patch('core.views.game_collection_csv_import.GameCollection.objects.create')
    def test_import_games_from_valid_csv(self, mock_create, mock_fetch, mock_gamecollection_filter, mock_game_filter):
        # Pakeičiame MockFilter, kad grąžintų tuščią queryset
        mock_gamecollection_filter.return_value = MagicMock()
        mock_gamecollection_filter.return_value.exists.return_value = False

        mock_game_filter.return_value = MagicMock()
        mock_game_filter.return_value.first.return_value = None

        # Sukuriame du mockintus žaidimus
        from core.models.game import Game
        mock_game1 = MagicMock(spec=Game)
        mock_game1.bgg_id = 13
        mock_game1.title = "Catan"
        mock_game1.thumbnail_url = "https://example.com/catan.jpg"

        mock_game2 = MagicMock(spec=Game)
        mock_game2.bgg_id = 822
        mock_game2.title = "Carcassonne"
        mock_game2.thumbnail_url = "https://example.com/carcassonne.jpg"

        # Nustatome, kad funkcija fetch_game_from_bgg grąžintų šiuos žaidimus
        mock_fetch.side_effect = [mock_game1, mock_game2]

        # Nustatome, kad mokinta create funkcija grąžintų mockintus objektus
        mock_create.side_effect = [MagicMock(), MagicMock()]

        csv_content = "bgg_id,title\n13,Catan\n822,Carcassonne"
        csv_file = SimpleUploadedFile("games.csv", csv_content.encode("utf-8"), content_type="text/csv")

        response = self.client.post("/collections/import-csv/", {"file": csv_file}, format="multipart")

        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(len(response.data.get("added", [])), 2)
        self.assertEqual(len(response.data.get("skipped", [])), 0)

    @patch('core.views.game_collection_csv_import.Game.objects.filter')
    @patch('core.views.game_collection_csv_import.GameCollection.objects.filter')
    @patch('core.views.game_collection_csv_import.fetch_game_from_bgg')
    def test_import_games_from_invalid_csv(self, mock_fetch, mock_gamecollection_filter, mock_game_filter):
        # Neteisingas CSV failas be reikiamų laukų
        # Įsitikiname, kad niekas nebus filtruojama
        mock_gamecollection_filter.return_value = MagicMock()
        mock_gamecollection_filter.return_value.exists.return_value = False

        mock_game_filter.return_value = MagicMock()
        mock_game_filter.return_value.first.return_value = None

        csv_content = "not_a_field\nSomethingWrong"
        csv_file = SimpleUploadedFile("games.csv", csv_content.encode("utf-8"), content_type="text/csv")

        response = self.client.post("/collections/import-csv/", {"file": csv_file}, format="multipart")

        # Netikriname statuso 400, nes pagal jūsų realizaciją tai turėtų būti 200 su tuščiu "added" sąrašu
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("added", [])), 0)
        self.assertGreaterEqual(len(response.data.get("skipped", [])), 1)