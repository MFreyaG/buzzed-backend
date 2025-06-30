from django.core.exceptions import ValidationError
from django.test import TestCase

from drink.models import FavoriteDrink, RawDrink, StoreDrink
from user.models import User


class FavoriteDrinkTestCase(TestCase):
    fixtures = [
        "addresses.json",
        "users.json",
        "ingredients.json",
        "base_drinks.json",
        "stores.json",
        "store_drinks.json",
        "raw_drinks.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk="11111111-1111-4111-a111-000000000001")

    def test_create_favorite_store_drink(self):
        store_drink = StoreDrink.objects.get(pk=1)

        FavoriteDrink.objects.create(user=self.user, store_drink=store_drink)
        favorite_drink = FavoriteDrink.objects.get(user=self.user)

        self.assertEqual(favorite_drink.store_drink.name, store_drink.name)
        self.assertEqual(favorite_drink.store_drink.store, store_drink.store)

    def test_create_favorite_raw_drink(self):
        raw_drink = RawDrink.objects.get(pk=2)

        FavoriteDrink.objects.create(user=self.user, raw_drink=raw_drink)
        favorite_drink = FavoriteDrink.objects.get(user=self.user)

        self.assertEqual(favorite_drink.raw_drink.name, raw_drink.name)
        self.assertEqual(favorite_drink.raw_drink.store_name, raw_drink.store_name)

    def test_favorite_drink_without_drinks_error(self):
        favorite_drink = FavoriteDrink(user=self.user)

        with self.assertRaises(ValidationError):
            favorite_drink.full_clean()

    def test_favorited_drink_is_preserved_when_store_drink_is_deleted(self):
        store_drink = StoreDrink.objects.get(pk=1)

        favorite_drink = FavoriteDrink.objects.create(
            user=self.user, store_drink=store_drink
        )
        self.assertEqual(favorite_drink.store_drink, store_drink)
        self.assertIsNone(favorite_drink.raw_drink)

        drink_name = store_drink.name
        store_name = store_drink.store.name
        ingredient_names = [
            ingredient.name for ingredient in store_drink.ingredients.all()
        ]
        alcohol_percentage = store_drink.alcohol_percentage
        store_drink.store.delete()
        favorite_drink.refresh_from_db()

        raw_drink_ingredient_names = [
            ingredient.name for ingredient in favorite_drink.raw_drink.ingredients.all()
        ]
        self.assertCountEqual(raw_drink_ingredient_names, ingredient_names)

        self.assertEqual(favorite_drink.raw_drink.name, drink_name)
        self.assertEqual(favorite_drink.raw_drink.store_name, store_name)
        self.assertEqual(
            favorite_drink.raw_drink.alcohol_percentage, alcohol_percentage
        )
        self.assertIsNone(favorite_drink.store_drink)
