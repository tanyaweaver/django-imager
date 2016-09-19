from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


@python_2_unicode_compatible
class ImagerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
    )
    camera_type = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    type_of_photography = models.CharField(max_length=200, blank=True)
    social_media = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return 'ImagerProfile for {}'.format(self.user)

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def active(self):
        return ImagerProfile.objects.filter(user__is_active=True)

    @receiver(post_save, sender=User)
    def update_imager_profile(sender, **kwargs):
        if not ImagerProfile(user=kwargs['instance']):
            ImagerProfile(
                user=kwargs['instance']
            ).save()
