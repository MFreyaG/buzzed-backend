from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class AddressTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        user1 = User.objects.get(pk=2)
        self.client.force_authenticate(user=user1)
        address_data = {
            "country": "United States",
            "state": "Nevada",
            "city": "Rachel",
            "neighborhood": "",
            "street": "Groom Lake Road",
            "number": "",
            "complement": "Near Nellis Air Force Range",
            "postal_code": "89003",
        }
        response = self.client.post(
            reverse("address"), data=address_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in response.data:
            self.assertEqual(response.data[key], address_data[key])

    def test_create_more_user_address_raises_exception(self):
        address_data = {
            "country": "United States",
            "state": "Nevada",
            "city": "Rachel",
            "neighborhood": "",
            "street": "Groom Lake Road",
            "number": "",
            "complement": "Near Nellis Air Force Range",
            "postal_code": "89003",
        }
        response = self.client.post(
            reverse("address"), data=address_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_address(self):
        address_data = {"city": "Nova Lima", "street": "Rua das Flores", "number": "80"}
        response = self.client.put(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], "Brazil")
        for key in address_data:
            self.assertEqual(response.data[key], address_data[key])

    def test_wrong_address_data_does_not_update_data(self):
        address_data = {"city": None, "street": "", "number": " "}
        response = self.client.put(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Belo Horizonte")
        self.assertEqual(response.data["neighborhood"], "Savassi")
        self.assertEqual(response.data["number"], "1000")
