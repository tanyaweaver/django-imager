from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os
import random
from imagersite.settings import BASE_DIR
from django.views.generic.base import TemplateView
from imager_images.models import Photo


class HomeView(TemplateView):
    template_name = 'imagersite/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            photo = Photo.objects.all().order_by('?').first().photo.url
            context['cover_path'] = photo
        except AttributeError:
            context['cover_path'] = 'static/images/tanyastree.jpeg'
        return context


# def home_view(request):
#     photo_filter = ['pu']
#     if request.id.is_authenticated:
#         photo_filter.append('sh')
#     photo = Photo.objects.filter(published__in=photo_filter).order_by('?').first()
#     return render(request, 'imagersite/home.html', {'photo': photo})

# def home_view(request):
#     # photo = Photo.objects.filter(published='pub').order_by('?').first()
#     # photo = Photo.objects.all().order_by('?').first().photo.url
#     # if not photo:
#     photo = os.path.join(MEDIA_ROOT, 'user_photos/mount.JPG')
#     #import pdb; pdb.set_trace()
#     return render(request, 'imagersite/home.html', {'photo': photo})
# def home_view(request):
#     """Returns image chosen at random from user photos or stock photo."""
#     # return render(request, 'imagersite/home.html')
#     list_of_user_photos = os.listdir(os.path.join(
#         BASE_DIR, 'media', 'user_photos'
#         )
#     )
#     if len(list_of_user_photos) != 0:
#         random_photo = random.choice(list_of_user_photos)
#         cover_path = os.path.join('media/user_photos', random_photo)
#     else:
#         cover_path = os.path.join('imagersite/static/images/tanyastree.jpeg')
#     return render(request, 'imagersite/home.html', {'cover_path': cover_path})
