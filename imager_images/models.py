from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
# from imager_profile.models import ImagerProfile


@python_2_unicode_compatible
class Photo(models.Model):
    user = models.ForeignKey(
        User,
        related_name="photos",
        on_delete=models.CASCADE
    )
    is_cover = models.BooleanField(default=False)
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


@python_2_unicode_compatible
class Album(models.Model):
    user = models.ForeignKey(
        User,
        related_name="albums",
        on_delete=models.CASCADE
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='albums',
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

    @property
    def cover(self):
        return self.objects.filter(photo__is_cover=True)

    def __str__(self):
        return 'Album for {}'.format(self.user)
