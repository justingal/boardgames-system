from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Organization, Membership

class JoinOrganizationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="member", password="Labas123!")
        self.org = Organization.objects.create(
            name="Prisijungimo klubas",
            description="Testinė",
            privacy="public",
            created_by=self.user,
            city="vilnius"
        )

    def authenticate(self):
        response = self.client.post("/token/", {
            "username": "member",
            "password": "Labas123!"
        }, format='json')
        self.assertIn(response.status_code, [200, 201])

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_user_can_join_organization(self):
        self.authenticate()
        response = self.client.post(f"/organizations/{self.org.id}/join/")
        self.assertIn(response.status_code, [200, 201])

        self.assertTrue(
            Membership.objects.filter(user=self.user, organization=self.org).exists()
        )

    def test_unauthenticated_user_cannot_join(self):
        response = self.client.post(f"/organizations/{self.org.id}/join/")
        self.assertEqual(response.status_code, 401)  # Teisingas statusas
