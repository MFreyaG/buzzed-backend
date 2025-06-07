import json

from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from store.models import Store
from user.models import User


class StoreTestCase(APITestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=4)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_store(self):
        response = self.client.get(reverse("", args=[]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        breakpoint()
