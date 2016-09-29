from django.shortcuts import render
from django.views.generic import UpdateView
from imager_profile.models import ImagerProfile
from django.urls import reverse


class EditProfileView(UpdateView):
    """Define edit profile class."""
    template_name = 'imager_profile/edit_profile_page.html'
    model = ImagerProfile
    fields = [
        'camera_type',
        'address',
        'website',
        'type_of_photography',
        'social_media'
    ]

    def get_success_url(self):
        """Set redirection after updating the album."""
        url = reverse('profile_view')
        return url
