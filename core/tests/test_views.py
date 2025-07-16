from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Address
from user.models import User


class AddressTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(username="spongebob")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        user1 = User.objects.get(username="elliewilliams")
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
        address = Address.objects.get(postal_code=address_data["postal_code"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["country"], address.country)
        self.assertEqual(response.data["city"], address.city)
        self.assertEqual(response.data["number"], address.number)
        self.assertEqual(response.data["postal_code"], address.postal_code)

    def test_create_address_with_wrong_data_raises_bad_request(self):
        address_data = {
            "country": None,
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


class AddressDetailTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(username="spongebob")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.address = Address.objects.get(pk="11111111-1111-4111-a111-000000000001")

    def test_get_address(self):
        response = self.client.get(
            reverse("address-detail", args=["11111111-1111-4111-a111-000000000001"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], self.address.country)
        self.assertEqual(response.data["city"], self.address.city)
        self.assertEqual(response.data["number"], self.address.number)
        self.assertEqual(response.data["postal_code"], self.address.postal_code)

    def test_get_address_with_wrong_pk_raises_not_found(self):
        response = self.client.get(
            reverse("address-detail", args=["55555555-5555-4555-a555-000000000005"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_address(self):
        updated_address_data = {"state": "Bermuda Triangle", "city": "Atlantis"}
        response = self.client.patch(
            reverse("address-detail", args=["11111111-1111-4111-a111-000000000001"]),
            data=updated_address_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(response.data["country"], self.address.country)
        self.assertEqual(updated_address_data["state"], self.address.state)
        self.assertEqual(updated_address_data["city"], self.address.city)

    def test_update_address_with_wrong_pk_raises_not_found(self):
        address_data = {"city": None, "street": "", "number": " "}
        response = self.client.patch(
            reverse("address-detail", args=["55555555-5555-4555-a555-000000000005"]),
            data=address_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_address_with_wrong_data_raises_forbidden(self):
        address_data = {"city": None, "street": "", "number": " "}
        response = self.client.patch(
            reverse("address-detail", args=["11111111-1111-4111-a111-000000000001"]),
            data=address_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
