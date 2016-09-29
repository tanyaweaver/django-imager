from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from imager_images.views import (
    LibraryView,
    PhotoView,
    AlbumView,
    UploadPhotoView,
    AddAlbumView,
    EditAlbumView,
    EditPhotoView,
    )


urlpatterns = [
    url(r'^library/',
        login_required(LibraryView.as_view()),
        name='library'),
    url(r'^photos/(?P<pk>\d+)/$',
        login_required(PhotoView.as_view()),
        name='photos'),
    url(r'^albums/(?P<pk>\d+)/$',
        login_required(AlbumView.as_view()),
        name='albums'),
    url(r'^photos/add/$',
        login_required(UploadPhotoView.as_view()),
        name='photo_add'),
    url(r'^albums/add/$',
        login_required(AddAlbumView.as_view()),
        name='album_add'),
    url(r'^albums/(?P<pk>\d+)/edit/$',
        login_required(EditAlbumView.as_view()),
        name='album_edit'),
    url(r'^photos/(?P<pk>\d+)/edit$',
        login_required(EditPhotoView.as_view()),
        name='photo_edit'),
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
