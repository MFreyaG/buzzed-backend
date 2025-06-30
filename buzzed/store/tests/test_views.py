from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from store.models import Store
from user.models import User


class StoreTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "stores.json"]

    def setUp(self):
        self.store_pk = "11111111-1111-4111-a111-000000000001"
        self.user = User.objects.get(pk=self.store_pk)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class StoreDetailTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "stores.json"]

    def setUp(self):
        self.store = Store.objects.get(pk="11111111-1111-4111-a111-000000000001")
        self.user = User.objects.get(username="spongebob")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_store(self):
        response = self.client.get(
            reverse("store-detail", args=[self.store.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.store.id), response.data["id"])
        self.assertEqual(self.store.name, response.data["name"])
        self.assertEqual(self.store.description, response.data["description"])
        self.assertEqual(self.store.icon_url, response.data["icon_url"])
        self.assertEqual(
            self.store.address.country, response.data["address"]["country"]
        )
        self.assertEqual(self.store.address.street, response.data["address"]["street"])
        self.assertEqual(self.store.address.number, response.data["address"]["number"])

    def test_get_store_with_wrong_id_raises_not_found(self):
        response = self.client.get(
            reverse("store-detail", args=["11111111-1111-4111-a111-000000000002"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_store(self):
        store_data = {
            "name": "Chum Bucket",
            "description": "Way better than The Krusty Krab!",
        }
        response = self.client.patch(
            reverse("store-detail", args=[self.store.pk]),
            data=store_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(store_data["name"], response.data["name"])
        self.assertEqual(store_data["description"], response.data["description"])
        self.assertEqual(self.store.icon_url, response.data["icon_url"])

    def test_update_store_with_user_without_permission_raises_forbidden(self):
        user2 = User.objects.get(username="barneystinson")
        self.client.force_authenticate(user=user2)
        store_data = {
            "name": "Chum Bucket",
            "description": "Way better than The Krusty Krab!",
        }
        response = self.client.patch(
            reverse("store-detail", args=[self.store.pk]),
            data=store_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.store.name, "The Krusty Krab")
        self.assertEqual(self.store.description, "Home of the Krabby Patty!")

    def test_update_store_with_wrong_id_raises_not_found(self):
        store_data = {
            "name": "Chum Bucket",
            "description": "Way better than The Krusty Krab!",
        }
        response = self.client.patch(
            reverse("store-detail", args=["11111111-1111-4111-a111-000000000002"]),
            data=store_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_store(self):
        response = self.client.delete(
            reverse("store-detail", args=[self.store.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Store.objects.filter(pk=self.store.pk).exists())

    def test_delete_store_with_user_without_permission_raises_forbidden(self):
        user2 = User.objects.get(username="johnsnow")
        self.client.force_authenticate(user=user2)
        response = self.client.delete(
            reverse("store-detail", args=[self.store.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_store_with_wrong_id_raises_not_found(self):
        response = self.client.delete(
            reverse("store-detail", args=["11111111-1111-4111-a111-000000000002"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
