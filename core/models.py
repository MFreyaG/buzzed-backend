import uuid

from django.db import models


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=10, blank=True)
    complement = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
