from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os
import random
from imagersite.settings import BASE_DIR
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'imagersite/home.html'

    def get_context_data(self, **kwargs):
        #import pdb; pdb.set_trace()
        context = super(HomeView, self).get_context_data(**kwargs)
        context['cover_path'] = 'media/david_banks_photo.jpg'
        return context

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
