from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import Contact, User


class UserDetailTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_data(self):
        response = self.client.get(
            reverse("user-detail", args=[self.user.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, response.data["username"])
        self.assertEqual(self.user.email, response.data["email"])
        self.assertEqual(self.user.first_name, response.data["first_name"])
        self.assertEqual(self.user.last_name, response.data["last_name"])
        self.assertEqual(self.user.icon_url, response.data["icon_url"])

    def test_get_nonexistent_user_data_raises_not_found(self):
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
        response = self.client.patch(
            reverse("user-detail", args=[self.user.pk]), data=user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(user_data["username"], self.user.username)
        self.assertEqual(user_data["first_name"], self.user.first_name)
        self.assertEqual(user_data["last_name"], self.user.last_name)
        self.assertEqual(user_data["icon_url"], self.user.icon_url)

    def test_update_not_authenticated_user_data_raises_forbidden(self):
        user = User.objects.get(pk="22222222-2222-4222-a222-000000000002")
        updated_user_data = {
            "username": "newtestname",
            "first_name": "Test",
            "last_name": "User",
            "icon_url": "https://newtesturl.com",
        }
        response = self.client.patch(
            reverse("user-detail", args=[user.pk]),
            data=updated_user_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user.refresh_from_db()
        self.assertNotEqual(user.username, updated_user_data["username"])
        self.assertNotEqual(user.first_name, updated_user_data["first_name"])
        self.assertNotEqual(user.last_name, updated_user_data["last_name"])
        self.assertNotEqual(user.icon_url, updated_user_data["icon_url"])

    def test_update_nonexistent_user_data_raises_not_found(self):
        response = self.client.get(
            reverse("user-detail", args=["00000000-0000-0000-0000-000000000000"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "contacts.json"]

    def setUp(self):
        self.user = User.objects.get(username="spongebob")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_followed_contacts(self):
        response = self.client.get(reverse("user-contacts"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_contacts = Contact.objects.filter(follower=self.user)
        self.assertEqual(len(user_contacts), len(response.data))

    def test_create_contact(self):
        contact_data = {"followed": "33333333-3333-4333-a333-000000000003"}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.get(pk=response.data["id"])
        self.assertEqual(contact.follower.pk, response.data["follower"])
        self.assertEqual(contact.followed.pk, response.data["followed"])

    def test_create_user_with_invalid_data(self):
        contact_data = {}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_same_user_contact(self):
        contact_data = {"followed": "22222222-2222-4222-a222-000000000002"}
        response = self.client.post(
            reverse("user-contacts"),
            data=contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_delete_contact(self):
        followed_uuid = "11111111-1111-4111-a111-000000000001"
        delete_contact_data = {"followed": followed_uuid}
        response = self.client.delete(
            reverse("user-contacts"),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Contact.objects.filter(
                follower_id=self.user.id, followed_id=followed_uuid
            ).exists()
        )

    def test_delete_non_existing_contact(self):
        delete_contact_data = {"followed": "33333333-3333-4333-a333-000000000003"}
        response = self.client.delete(
            reverse("user-contacts"),
            data=delete_contact_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
