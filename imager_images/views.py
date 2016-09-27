from django.shortcuts import render
from django.views.generic import TemplateView


class LibraryView(TemplateView):
    template_name = 'imager_images/1.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        current_user = self.request.user
        # all albums by this user in reverse alpha order.
        albums_by_name = current_user.albums.order_by('-date_uploaded')
        # all photos byt his user ordered by upload date, in reverse.
        photos_by_date = current_user.photos.order_by('-date_uploaded')
        context['albums'] = albums_by_name
        context['photos'] = photos_by_date
        return context
