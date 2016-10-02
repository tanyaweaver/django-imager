from django.utils.encoding import python_2_unicode_compatible
from django.views.generic.base import TemplateView
from imager_images.models import Photo


@python_2_unicode_compatible
class HomeView(TemplateView):
    template_name = 'imagersite/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            photo = Photo.objects.filter(published='pu').order_by('?').first()
            photo_url = photo.photo.url
            context['cover_path'] = photo_url
        except AttributeError:
            context['cover_path'] = 'static/images/tanyastree.jpeg'
        return context
