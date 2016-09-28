from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from imager_images.views import LibraryView, PhotoView, AlbumView


urlpatterns = [
    url(r'^library/',
        login_required(LibraryView.as_view()),
        name='library'),
    url(r'^photos/(?P<pk>\d+)/$',
        login_required(PhotoView.as_view()),
        name='photos'),
    url(r'^album/(?P<pk>\d+)/$',
        login_required(AlbumView.as_view()),
        name='albums'),
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
