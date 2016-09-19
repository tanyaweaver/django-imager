from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
form imager_profile import ImagerProfile


# Create your models here.


@python_2_unicode_compatible
class Photo(models.Model):
    profile = models.ForeignKey(
        ImagerProfile,
        related_name="photos",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    date_uploaded = models.DateField(auto_now_add=True)
    data_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now=True)
    private = 'pr'
    shared = 'sh'
    public = 'pu'
    published = models.CharField(
        max_length=2,
        choices=(
            (private, 'private'),
            (shared, 'shared'),
            (public, 'public')
            ),
        default=private,
        blank=True
        )
    photo = models.ImageField(
        upload_to='user_photos',
        blank=True,
        null=True
    )

    def __str__(self):
        return 'Photo for {}'.format(self.user)
