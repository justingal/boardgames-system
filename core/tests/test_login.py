from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Labas123!"
        )

    def test_login_success(self):
        response = self.client.post("/token/", {
            "username": "testuser",
            "password": "Labas123!"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        response = self.client.post("/token/", {
            "username": "testuser",
            "password": "blogas"
        }, format='json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)
