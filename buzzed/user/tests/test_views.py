from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import Contact, User


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


class UserDetailTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_data(self):
        response = self.client.get(reverse("user-detail", args=[self.user.pk]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, response.data["username"])
        self.assertEqual(self.user.email, response.data["email"])
        self.assertEqual(self.user.first_name, response.data["first_name"])
        self.assertEqual(self.user.last_name, response.data["last_name"])
        self.assertEqual(self.user.icon_url, response.data["icon_url"])

    def test_get_nonexistent_user_data_raises_exception(self):
        response = self.client.get(
            reverse("user-detail", args=["00000000-0000-0000-0000-000000000000"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_data(self):
        user_data = {
            "username": "newtestname",
            "first_name": "Test",
            "last_name": "User",
            "icon_url": "https://newtesturl.com",
        }
        response = self.client.put(
            reverse("user-detail", args=[self.user.pk]), data=user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(user_data["username"], self.user.username)
        self.assertEqual(user_data["first_name"], self.user.first_name)
        self.assertEqual(user_data["last_name"], self.user.last_name)
        self.assertEqual(user_data["icon_url"], self.user.icon_url)

    def test_update_other_user_data_raises_exception(self):
        user = User.objects.get(pk="22222222-2222-4222-a222-000000000002")
        updated_user_data = {
            "username": "newtestname",
            "first_name": "Test",
            "last_name": "User",
            "icon_url": "https://newtesturl.com",
        }
        response = self.client.put(
            reverse("user-detail", args=[user.pk]), data=updated_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user.refresh_from_db()
        self.assertNotEqual(user.username, updated_user_data["username"])
        self.assertNotEqual(user.first_name, updated_user_data["first_name"])
        self.assertNotEqual(user.last_name, updated_user_data["last_name"])
        self.assertNotEqual(user.icon_url, updated_user_data["icon_url"])

    def test_update_nonexistent_user_data_raises_exception(self):
        response = self.client.get(
            reverse("user-detail", args=["00000000-0000-0000-0000-000000000000"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "contacts.json"]

    def setUp(self):
        self.user = User.objects.get(pk="22222222-2222-4222-a222-000000000002")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_followed_contacts(self):
        response = self.client.get(reverse("user-contacts"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_contacts = Contact.objects.filter(user1=self.user)
        self.assertEqual(len(user_contacts), len(response.data))

    def test_create_contact(self):
        contact_data = {"user2": "33333333-3333-4333-a333-000000000003"}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.get(id=response.data["id"])
        self.assertEqual(contact.user1.pk, response.data["follower"])
        self.assertEqual(contact.user2.pk, response.data["followed"])

    def test_create_user_with_invalid_data(self):
        contact_data = {}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_same_user_contact(self):
        contact_data = {"user2": "22222222-2222-4222-a222-000000000002"}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_delete_contact(self):
        user2_uuid = "11111111-1111-4111-a111-000000000001"
        delete_contact_data = {"user2": user2_uuid}
        response = self.client.delete(
            reverse("user-contacts"),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Contact.objects.filter(user1_id=self.user.id, user2_id=user2_uuid).exists()
        )

    def test_delete_non_existing_contact(self):
        delete_contact_data = {"user2": "33333333-3333-4333-a333-000000000003"}
        response = self.client.delete(
            reverse("user-contacts"),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)