from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
   url(r'^$',
       login_required(TemplateView.as_view(
           template_name='imager_profile/profile_view.html'
       )),
       name='profile_view'),
   ]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
       settings.MEDIA_URL,
       document_root=settings.MEDIA_ROOT)
