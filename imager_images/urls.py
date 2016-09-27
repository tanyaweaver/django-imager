from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from imager_images.models import Photo, Album


urlpatterns = [
    url(r'^library/', TemplateView.as_view(
        template_name='imager_images/library_view.html'
        ), name='library'),
    url(r'^photos/(?P<pk>\d+)/$', DetailView.as_view(
        template_name='imager_images/image_view.html',
        model=Photo,
        context_object_name='photo'
        ), name='photos'),
    url(r'^albums/(?P<pk>\d+)/$', DetailView.as_view(
        template_name='imager_images/album_view.html',
        model=Album,
        context_object_name='album'
        ), name='albums'),
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
