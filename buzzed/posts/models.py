from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from drinks.models import StoreDrink, RawDrink
from users.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_drink = models.ForeignKey(StoreDrink, on_delete=models.SET_NULL, null=True, blank=True)
    raw_drink = models.ForeignKey(RawDrink, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        if not self.store_drink and not self.raw_drink:
            raise ValidationError("FavoriteDrink needs a raw_drink or store_drink value.")

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()

class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.URLField()