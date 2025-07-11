from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from drink.models import Drink, FavoriteDrink, Ingredient
from store.models import Store
from user.models import User


class DrinkTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="johnsnow")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.store = Store.objects.get(name="The Krusty Krab")

    def test_get_drinks(self):
        filter_data = {"store": self.store.pk}
        response = self.client.get(reverse("drink"), data=filter_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Jellyfish Juice")
        self.assertEqual(response.data[0]["store"]["name"], self.store.name)

    def test_post_drink(self):
        ingredients = Ingredient.objects.filter(
            name__in=["Pineapple Juice", "Whiskey", "Lemon Juice"]
        )
        drink_data = {
            "name": "Kelp punch",
            "store": self.store.pk,
            "description": "For nights out in bikini bottom",
            "price": "50.00",
            "alcohol_percentage": "23%",
            "image_url": "https://example.com/kelp-punch.jpg",
            "ingredients": [ingredient.pk for ingredient in ingredients],
        }
        response = self.client.post(reverse("drink"), data=drink_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        drink = Drink.objects.get(name=drink_data["name"])
        self.assertEqual(response.data["name"], drink.name)
        self.assertEqual(response.data["store"], self.store.pk)
        self.assertEqual(
            response.data["ingredients"], [ingredient.pk for ingredient in ingredients]
        )

    def test_post_drink_with_invalid_data_raises_bad_request(self):
        ingredients = Ingredient.objects.filter(
            name__in=["Pineapple Juice", "Whiskey", "Lemon Juice"]
        )
        drink_data = {
            "name": "Kelp punch",
            "store": self.store.pk,
            "description": "For nights out in bikini bottom",
            "price": "50.00",
            "alcohol_percentage": "23%",
            "image_url": "example.com/kelp-punch.jpg",
            "ingredients": [ingredient.pk for ingredient in ingredients],
        }
        response = self.client.post(reverse("drink"), data=drink_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DrinkDetailTestCase(APITestCase):
    fixtures = [
        "ingredients.json",
        "addresses.json",
        "users.json",
        "stores.json",
        "drinks.json",
    ]

    def setUp(self):
        self.drink = Drink.objects.get(name="The Suit Up")
        self.user = User.objects.get(username="barneystinson")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_drink(self):
        response = self.client.get(
            reverse("drink-detail", args=[self.drink.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.drink.name)
        self.assertEqual(
            response.data["alcohol_percentage"], self.drink.alcohol_percentage
        )
        self.assertEqual(response.data["store"]["name"], self.drink.store.name)
        self.assertEqual(len(response.data["ingredients"]), 3)

    def test_get_drink_with_wrong_pk_raises_not_found(self):
        response = self.client.get(
            reverse("drink-detail", args=["44444444-4444-4444-a444-000000000005"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_drink(self):
        drink_data = {"description": "Almost a slap on your face!", "price": "35.00"}
        response = self.client.patch(
            reverse("drink-detail", args=[self.drink.pk]),
            data=drink_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.drink.refresh_from_db()
        self.assertEqual(response.data["name"], self.drink.name)
        self.assertEqual(response.data["description"], drink_data["description"])
        self.assertEqual(response.data["price"], drink_data["price"])
        self.assertEqual(self.drink.description, drink_data["description"])

    def test_update_drink_with_wrong_data_raises_bad_request(self):
        drink_data = {"description": None, "price": "35.00"}
        response = self.client.patch(
            reverse("drink-detail", args=[self.drink.pk]),
            data=drink_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_drink_with_wrong_pk_raises_not_found(self):
        drink_data = {"description": "Almost a slap on your face!", "price": "35.00"}
        response = self.client.patch(
            reverse("drink-detail", args=["44444444-4444-4444-a444-000000000005"]),
            data=drink_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_drink(self):
        response = self.client.delete(
            reverse("drink-detail", args=[self.drink.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Drink.objects.filter(pk=self.drink.pk).exists())

    def test_delete_drink_with_wrong_pk_raises_not_found(self):
        response = self.client.delete(
            reverse("drink-detail", args=["44444444-4444-4444-a444-000000000005"]),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FavoriteDrinkTestCase(APITestCase):
    fixtures = [
        "addresses.json",
        "users.json",
        "stores.json",
        "ingredients.json",
        "drinks.json",
        "favorite_drinks.json",
    ]

    def setUp(self):
        self.drink = Drink.objects.get(name="Winterfell Mulled Wine")
        self.user = User.objects.get(username="johnsnow")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_favorite_drinks(self):
        drink = Drink.objects.get(name="Firefly Cocktail")
        filter_data = {"user": self.user.pk}
        response = self.client.get(
            reverse("favorite-drink"), data=filter_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["user"], self.user.pk)
        self.assertEqual(response.data[0]["drink"], drink.pk)

    def test_post_favorite_drink(self):
        favorite_drink_data = {"user": self.user.pk, "drink": self.drink.pk}
        response = self.client.post(
            reverse("favorite-drink"), data=favorite_drink_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FavoriteDrink.objects.filter(user=self.user, drink=self.drink).exists()
        )

    def test_post_favorite_drink_with_invalid_data_raises_bad_request(self):
        favorite_drink_data = {"user": None, "drink": self.drink.pk}
        response = self.client.post(
            reverse("favorite-drink"), data=favorite_drink_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_favorite_drink(self):
        response = self.client.delete(
            reverse("favorite-drink-detail", args=[self.drink.pk]), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteDrink.objects.filter(pk=self.drink.pk).exists())

    def test_delete_favorite_drink_with_wrong_pk_raises_not_found(self):
        response = self.client.delete(
            reverse(
                "favorite-drink-detail", args=["44444444-4444-4444-a444-000000000005"]
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
