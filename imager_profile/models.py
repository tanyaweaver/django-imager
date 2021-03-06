from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class ImagerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
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

    @classmethod
    def active(cls):
        return ImagerProfile.objects.filter(user__is_active=True)


@receiver(post_save, sender=User)
def update_imager_profile(sender, **kwargs):
    if not ImagerProfile.objects.filter(user=kwargs['instance']):
        ImagerProfile(
            user=kwargs['instance']
        ).save()
