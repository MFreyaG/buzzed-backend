from django.core.exceptions import ValidationError
from django.test import TestCase

from drink.models import FavoriteDrink, RawDrink, StoreDrink
from user.models import User


class FavoriteDrinkTestCase(TestCase):
    fixtures = [
        "addresses.json",
        "users.json",
        "ingredients.json",
        "base_drink.json",
        "store.json",
        "store_drink.json",
        "raw_drink.json",
    ]

    def test_create_favorite_store_drink(self):
        user = User.objects.get(pk=1)
        store_drink = StoreDrink.objects.get(pk=1)

        FavoriteDrink.objects.create(user=user, store_drink=store_drink)
        favorite_drink = FavoriteDrink.objects.get(user=user)

        self.assertEqual(favorite_drink.store_drink.name, store_drink.name)
        self.assertEqual(favorite_drink.store_drink.store, store_drink.store)

    def test_create_favorite_raw_drink(self):
        user = User.objects.get(pk=1)
        raw_drink = RawDrink.objects.get(pk=2)

        FavoriteDrink.objects.create(user=user, raw_drink=raw_drink)
        favorite_drink = FavoriteDrink.objects.get(user=user)

        self.assertEqual(favorite_drink.raw_drink.name, raw_drink.name)
        self.assertEqual(favorite_drink.raw_drink.store_name, raw_drink.store_name)

    def test_avorite_drink_without_drinks_error(self):
        user = User.objects.get(pk=1)
        favorite_drink = FavoriteDrink(user=user)

        with self.assertRaises(ValidationError):
            favorite_drink.full_clean()

    def test_favorite_drink_persists_with_store_deletion(self):
        user = User.objects.get(pk=1)
        store_drink = StoreDrink.objects.get(pk=1)

        favorite_drink = FavoriteDrink.objects.create(
            user=user, store_drink=store_drink
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
