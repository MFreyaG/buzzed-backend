from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from drink.models import Drink
from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    review = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.URLField()
