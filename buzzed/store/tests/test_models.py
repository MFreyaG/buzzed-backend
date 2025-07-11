from django.test import TestCase

from drink.models import Drink
from store.models import Store


class StoreTestCase(TestCase):
    fixtures = [
        "addresses.json",
        "users.json",
        "stores.json",
        "ingredients.json",
        "drinks.json",
    ]

    def setUp(self):
        self.store = Store.objects.get(pk="33333333-3333-4333-a333-000000000003")

    def test_delete_store_replaces_store_field_on_drink_to_store_name(self):
        store_name = self.store.name
        drink = Drink.objects.get(store=self.store)
        self.assertEqual(drink.store, self.store)
        self.assertEqual(drink.store_name, "")
        self.store.delete()
        drink.refresh_from_db()
        self.assertEqual(drink.store, None)
        self.assertEqual(drink.store_name, store_name)
