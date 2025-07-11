import uuid

from django.core.exceptions import ValidationError
from django.db import models

from store.models import Store
from user.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Drink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    store_name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=20, blank=True)
    alcohol_percentage = models.CharField(max_length=10, blank=True)
    image_url = models.URLField(null=True, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient, related_name="%(class)s_ingredients", blank=True
    )

    def __str__(self):
        if self.store:
            return f"{self.name} - {self.store.name}"
        return f"{self.name} - {self.store_name}"


class FavoriteDrink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.drink.name}"
