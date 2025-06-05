from django.db.models.signals import pre_delete
from django.dispatch import receiver

from drinks.models import StoreDrink, RawDrink, FavoriteDrink

@receiver(pre_delete, sender=StoreDrink)
def create_raw_drink_before_deletion(sender, instance, **kwargs):
    raw_drink = RawDrink.objects.create(
        name=instance.name,
        store_name=instance.store.name,
        alcohol_percentage=instance.alcohol_percentage
    )
    raw_drink.ingredients.set(instance.ingredients.all())

    FavoriteDrink.objects.filter(store_drink=instance).update(
        raw_drink=raw_drink,
        store_drink=None
    )
