from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from imager_images.models import Photo, Album
from django.contrib.auth.decorators import login_required
from imager_images.views import LibraryView, PhotoView


urlpatterns = [
    url(r'^library/',
        login_required(LibraryView.as_view()),
        name='library'),
    # url(r'^photos/(?P<pk>\d+)/$',
    #     login_required(DetailView.as_view(
    #         template_name='imager_images/photo_view.html',
    #         model=Photo,
    #         context_object_name='photo'
    #     )),
    #     name='photos'),
    url(r'^photos/(?P<pk>\d+)/$',
        login_required(PhotoView.as_view()),
        name='photos'),
    url(r'^album/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            template_name='imager_images/album_view.html',
            model=Album,
            context_object_name='album'
        )),
        name='albums'),
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
