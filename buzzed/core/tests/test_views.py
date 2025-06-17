from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class AddressTestCase(APITestCase):
    fixtures = ["addresses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user_address = {
            "country": "Westeros",
            "state": "The North",
            "city": "The Wall",
            "neighborhood": "Castle Black",
            "street": "Castle Black Main Gate",
            "number": "1",
            "complement": "Headquarters of the Night's Watch",
            "postal_code": "NW001",
        }

    def test_create_address(self):
        user1 = User.objects.get(pk="33333333-3333-4333-a333-000000000003")
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
        address_data = {
            "city": "King's Landing",
            "street": "Red Keep street",
            "number": "80",
        }
        response = self.client.put(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], self.user_address["country"])
        for key in address_data:
            self.assertEqual(response.data[key], address_data[key])

    def test_wrong_address_data_does_not_update_data(self):
        address_data = {"city": None, "street": "", "number": " "}
        response = self.client.put(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], self.user_address["city"])
        self.assertEqual(
            response.data["neighborhood"], self.user_address["neighborhood"]
        )
        self.assertEqual(response.data["number"], self.user_address["number"])
