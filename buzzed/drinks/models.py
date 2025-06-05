from django.core.exceptions import ValidationError
from django.db import models

from stores.models import Store
from users.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

class BaseDrink(models.Model):
    name = models.CharField(max_length=50)
    alcohol_percentage = models.CharField(max_length=10, blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='%(class)s_ingredients', blank=True)
   
class StoreDrink(BaseDrink):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(null=True, blank=True)

class RawDrink(BaseDrink):
    store_name = models.CharField(max_length=50)

class FavoriteDrink(models.Model):
    store_drink = models.ForeignKey(StoreDrink, on_delete=models.SET_NULL, null=True, blank=True)
    raw_drink = models.ForeignKey(RawDrink, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        if not self.store_drink and not self.raw_drink:
            raise ValidationError("FavoriteDrink needs a raw_drink or store_drink value.")