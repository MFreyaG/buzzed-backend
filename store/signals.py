from django.db.models.signals import pre_delete
from django.dispatch import receiver

from drink.models import Drink

from .models import Store


@receiver(pre_delete, sender=Store)
def save_store_name_on_drink_deletion(sender, instance, **kwargs):
    Drink.objects.filter(store=instance).update(store_name=instance.name)
