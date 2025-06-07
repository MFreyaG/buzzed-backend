from django.db import models

from core.models import Address
from user.models import User


class Store(models.Model):
    name = models.CharField(max_length=50)
    doc_number = models.CharField(max_length=14)
    description = models.CharField(max_length=255, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    admins = models.ManyToManyField(User, related_name="admin_stores", blank=True)
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.doc_number} - {self.name}"
