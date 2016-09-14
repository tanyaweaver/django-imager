from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.


@python_2_unicode_compatible
class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile"
    )
    camera_type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    type_of_photography = models.CharField(max_length=200)
    social_media = models.CharField(max_length=200)

    def active():
        return User.objects.filter(is_active=True)

    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance):
    #     instance.profile = UserProfile()
    #     instance.profile.save()
