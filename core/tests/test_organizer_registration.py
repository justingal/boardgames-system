from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization

class OrganizerRegistrationTest(APITestCase):
    def test_register_organizer_and_organization(self):
        response = self.client.post("/register/organizer/", {
            "username": "orguser",
            "email": "org@example.com",
            "password": "Labas123!",
            "first_name": "Rokas",
            "last_name": "Organizatorius",
            "organization": {
                "name": "Konoha Strategy Club",
                "description": "Testinė organizacija",
                "privacy": "protected",
                "category": "classic_strategic",
                "city": "vilnius"
            }
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="orguser").exists())
        self.assertTrue(Organization.objects.filter(name="Konoha Strategy Club").exists())
