import json

from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from store.models import Store
from user.models import User


class StoreTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json", "stores.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.store = {
            "pk": 1,
            "name": "The Bastard's alley",
            "doc_number": "11223344556677",
            "description": "Grab something strong, winter is coming!",
            "address": 3,
            "manager": 1,
            "icon_url": "",
        }

    def test_get_store_data(self):
        response = self.client.get(
            reverse("store", args=[self.store["pk"]]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.store:
            self.assertEqual(self.store[key], response[key])

    def test_get_store_with_wrong_pk_raises_exception(self):
        response = self.client.get(reverse("store", args=[5]), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
