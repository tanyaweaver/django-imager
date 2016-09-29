from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView
from imager_images.models import Photo, Album
from django.urls import reverse


class LibraryView(TemplateView):
    """Establish class of view for library page."""
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
    """Establish class of view for photo page."""
    template_name = 'imager_images/photo_page.html'
    model = Photo
    context_object_name = 'photo'
    # pk_url_kwargs = "id"

    def get_context_data(self, **kwargs):
        """Return modified context for photo page."""
        context = super(PhotoView, self).get_context_data(**kwargs)
        published = self.object.published
        status_dict = {'pu': 'public', 'sh': 'shared', 'pr': 'private'}
        status = status_dict[published]
        context['status'] = status
        return context


class AlbumView(DetailView):
    """Establish class of view for album page."""
    template_name = 'imager_images/album_page.html'
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        """Return modified context for album page."""
        context = super(AlbumView, self).get_context_data(**kwargs)
        published = self.object.published
        status_dict = {'pu': 'public', 'sh': 'shared', 'pr': 'private'}
        status = status_dict[published]
        context['status'] = status
        return context


class UploadPhotoView(CreateView):
    """Establish class of view for uploading photos."""
    template_name = 'imager_images/upload_photo_page.html'
    model = Photo
    fields = ['title', 'description', 'photo']

    def get_success_url(self):
        """Set redirection upon successful upload."""
        url = reverse('library')
        return url

    def form_valid(self, form):
        """Modify form validation to apply a user to an instance."""
        form.instance.user = self.request.user
        return super(UploadPhotoView, self).form_valid(form)


class AddAlbumView(CreateView):
    """Establish class of view for adding albums."""
    template_name = 'imager_images/add_album_page.html'
    model = Album
    fields = ['title', 'description', 'photos', 'published']

    def get_form(self, form_class=None):
        form = super(AddAlbumView, self).get_form(form_class)
        qs = form.fields['photos'].queryset
        qs = qs.filter(user=self.request.user)
        form.fields['photos'].queryset = qs
        return form

    def get_success_url(self):
        """Set redirection upon addition of album."""
        url = reverse('library')
        return url

    def form_valid(self, form):
        """Assign a user attr to an instance."""
        form.instance.user = self.request.user
        return super(AddAlbumView, self).form_valid(form)
