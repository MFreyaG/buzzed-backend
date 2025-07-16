import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from core.models import Address


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=False
    )
    icon_url = models.URLField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed"
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError("A contact must have different users.")

    def __str__(self):
        return f"{self.follower.username} - {self.followed.username}"

    class Meta:
        unique_together = ("follower", "followed")
