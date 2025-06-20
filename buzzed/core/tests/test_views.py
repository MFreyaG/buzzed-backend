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
        self.assertDictEqual(response.data, address_data)

    def test_create_address_for_user_with_registered_address_raises_exception(self):
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
    
    def test_create_address_with_wrong_data_raises_exception(self):
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
        self.assertEqual(len(response.data), 1)

    def test_update_address(self):
        address_data = {
            "city": "King's Landing",
            "street": "Red Keep street",
            "number": "80",
        }
        response = self.client.patch(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country"], self.user_address["country"])
        self.assertEqual(response.data["city"], address_data["city"])
        self.assertEqual(response.data["street"], address_data["street"])
        self.assertEqual(response.data["number"], address_data["number"])

    def test_wrong_address_data_does_not_update_data(self):
        address_data = {"city": None, "street": "", "number": " "}
        response = self.client.patch(reverse("address"), data=address_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 2)