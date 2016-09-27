from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
   url(r'^$', TemplateView.as_view(
       template_name='imager_profile/profile_view.html'
       ), name='profile_home'),
   ]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
       settings.MEDIA_URL,
       document_root=settings.MEDIA_ROOT)
