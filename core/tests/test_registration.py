from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(APITestCase):
    def test_register_user_successfully(self):
        url = "/register/"  # jei nenaudoji reverse(name='register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Labas123!",
            "first_name": "Jonas",
            "last_name": "Jonaitis"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())
