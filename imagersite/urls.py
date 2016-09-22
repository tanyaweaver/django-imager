"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from imagersite.views import HomeView
import django.contrib.auth.views as dj
import registration
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from imager_profile.models import ImagerProfile
# from imagersite.views import home_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', home_view, name='homepage'),
    url(r'^$', HomeView.as_view(
        template_name='imagersite/home.html'
    ), name='homepage'),
    url(r'^accounts/',
        include('registration.backends.hmac.urls'),
        name='accounts'),
    # url(r'^$',
    #     TemplateView.as_view(template_name='imager_profile/profile.html'),
    #     name='personal_profile'
    #     ),
    # url(r'(?P<username>[a-f\0-9-]+)$',
    #     DetailView.as_view(
    #         template_name='imager_profile/public_profile',
    #         model=ImagerProfile,
    #         pk_url_kwargs=user_id,
    #         context_object_name='imager_profile'
    #     ),
    #     name='public_profile'
    #     )
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
