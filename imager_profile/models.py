from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    username = models.OneToOneField(
        User,
        unique=True,
        on_delete=models.CASCADE
    )
    camera_type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    type_of_photography = models.CharField(max_length=200)
    social_media = models.CharField(max_length=200)

    def active():
        return User.objects.filter(is_active=True)
