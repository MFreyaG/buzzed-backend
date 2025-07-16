from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from store.models import Store
from user.models import User


class StoreTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "stores.json"]

    def setUp(self):
        self.user = User.objects.get(username="johnsnow")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_store(self):
        filter_data = {"name": "The Bastard's alley"}
        response = self.client.get(reverse("store"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "The Bastard's alley")
        self.assertEqual(
            response.data[0]["description"], "Grab something strong, winter is coming!"
        )

    def test_post_store(self):
        store_data = {
            "name": "The White Walker",
            "doc_number": "12345678910",
            "manager": self.user.pk,
        }
        response = self.client.post(reverse("store"), data=store_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        store = Store.objects.get(pk=response.data["id"])
        self.assertEqual(store_data["name"], store.name)
        self.assertEqual(store_data["manager"], store.manager.pk)

    def test_post_store_with_wrong_data_raises_bad_request(self):
        store_data = {}
        response = self.client.post(reverse("store"), data=store_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, response.data["name"])
        self.assertEqual(self.store.description, response.data["description"])
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
