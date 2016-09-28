from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView
from imager_images.models import Photo, Album
from django.urls import reverse


class LibraryView(TemplateView):
    template_name = 'imager_images/library_page.html'

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


class PhotoView(DetailView):
    template_name = 'imager_images/photo_page.html'
    model = Photo
    context_object_name = 'photo'
    # pk_url_kwargs = "id"

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        published = self.object.published
        status_dict = {'pu': 'public', 'sh': 'shared', 'pr': 'private'}
        status = status_dict[published]
        context['status'] = status
        return context


class AlbumView(DetailView):
    template_name = 'imager_images/album_page.html'
    model = Album
    context_object_name = 'album'
    # pk_url_kwargs = "id"

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        published = self.object.published
        status_dict = {'pu': 'public', 'sh': 'shared', 'pr': 'private'}
        status = status_dict[published]
        context['status'] = status
        return context


class UploadPhotoView(CreateView):
        template_name = 'imager_images/upload_photo_page.html'
        model = Photo
        fields = ['title', 'description', 'photo', 'user']

        def get_success_url(self):
            url = self.object.photo.url
            return url
