from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        User.objects.create_user(
            username="TestUser", email="testuser@email.com", password="t3stp4assw0rd"
        )

    def test_valid_signup(self):
        signup_data = {
            "username": "NewUser",
            "email": "newuser@email.com",
            "password": "T3stP4as5w0rd",
        }
        response = self.client.post(reverse("signup"), data=signup_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(username=signup_data["username"])
        self.assertEqual(signup_data["username"], created_user.username)
        self.assertEqual(signup_data["email"], created_user.email)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_signup(self):
        signup_data = {
            "username": "NewUser",
            "email": "newuser@email.com",
            "password": "2Sh0rt",
        }
        response = self.client.post(reverse("signup"), data=signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_valid_login(self):
        login_data = {
            "email": "testuser@email.com",
            "password": "t3stp4assw0rd",
        }
        response = self.client.post(reverse("login"), data=login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials_login(self):
        login_data = {
            "email": "testuser@email.com",
            "password": "wrongpassword",
        }
        response = self.client.post(reverse("login"), data=login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_non_existent_user_login(self):
        non_existent_user_data = {
            "email": "nonexistent@email.com",
            "password": "t3stp4assw0rd",
        }
        response = self.client.post(
            reverse("login"), data=non_existent_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
