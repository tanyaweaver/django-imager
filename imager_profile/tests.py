from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from imager_images.models import Photo, Album
from django.urls import reverse
import os
from io import open
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PHOTO_PATH = os.path.join(HERE, 'test_resources', 'tree.jpg')
TEST_MEDIA_ROOT = tempfile.mkdtemp()


class ImagerProfileTestCase(TestCase):
    """Create test class for ImagerProfile model."""
    def setUp(self):
        """Set up a fake user and profile."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()

    def test_user_exists(self):
        """Prove the user exists."""
        self.assertTrue(self.user is not None)

    def test_username(self):
        """Prove the username is correct."""
        self.assertEqual(self.user.username, 'test', 'wrong username')

    def test_profile_exists(self):
        """Prove that the user has a profile."""
        self.assertTrue(self.user.profile is not None)

    def test_profile_is_attached_to_right_user(self):
        """Prove that the profileis attached to the right user."""
        self.assertEqual(self.user.profile.user.username, 'test')


class ProfileViewTestCase(TestCase):
    """Define class to test the view of profile."""
    def setUp(self):
        """Define setup for the test class."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.complete_profile()
        self.upload_photos_add_album()
        self.url = reverse('profile_view')
        self.response = self.client.get(self.url)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def upload_photos_add_album(self):
        """Upload photos and add albums for the user."""
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'user': self.user,
                'photo': fh,
                'title': 'photo1'
            }
            self.client.post(reverse('photo_add'), data)
        ph = Photo.objects.filter(user=self.user).first()
        data = {
            'title': 'album1',
            'photos': ph.pk,
            'user': self.user,
        }
        self.client.post(reverse('album_add'), data)

    def complete_profile(self):
        """Complete user's profile via <edit progfile> page."""
        data = {
            'user': self.user,
            'camera_type': 'canon',
            'type_of_photography': 'animals',
            'social_media': 'fb',
            'website': 'www.test.com'
        }
        self.client.post(
            reverse('profile_edit', kwargs={'pk': self.user.pk}),
            data
        )

    def test_auth_user_have_access_to_profile_view(self):
        """Prove that auth user has access to the profile view."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render profile page."""
        self.assertTemplateUsed(
            self.response,
            'imager_profile/profile_page.html'
        )

    def test_profile_edit_button_present(self):
        """Prove that <edit profile> button is present."""
        expected = 'href="{}"'.format(reverse(
            'profile_edit', kwargs={'pk': self.user.pk}))
        self.assertContains(self.response, expected)

    def test_right_number_of_photos_displayed(self):
        photos = Photo.objects.filter(user=self.user).count()
        albums = Album.objects.filter(user=self.user).count()
        self.assertContains(self.response, str(photos) + ' photos')
        self.assertContains(self.response, str(albums) + ' albums')

    def test_profile_info_displayed_correctly(self):
        attr = ['test', 'canon', 'animal', 'fb', 'www.test.com']
        for x in attr:
            self.assertContains(self.response, x)


class EditProfileTestCase(TestCase):
    """Define test case class for profile editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.complete_profile()
        self.url = reverse('profile_edit', kwargs={'pk': self.user.pk})
        self.response = self.client.get(self.url)

    def complete_profile(self):
        """Complete user's profile via <edit progfile> page."""
        data = {
            'user': self.user,
            'camera_type': 'canon',
            'type_of_photography': 'animals',
            'social_media': 'fb',
            'website': 'www.test.com'
        }
        self.client.post(
            reverse('profile_edit', kwargs={'pk': self.user.pk}),
            data
        )

    def test_auth_user_have_access_to_profile_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit profile page."""
        self.assertTemplateUsed(
            self.response,
            'imager_profile/edit_profile_page.html'
        )

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_update_from_edit_profile_page(self):
        """
        Prove redirection to the profile page after successfully updating
        the profile.
        """
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/profile/')

    def test_updated_info_shows_up(self):
        """Prove that updated profile info shows up on profile page."""
        # info before update
        attr = ['test', 'canon', 'animal', 'fb', 'www.test.com']
        response = self.client.get(reverse('profile_view'))
        for x in attr:
            self.assertContains(response, x)
        # updating info
        data = {
            'camera_type': 'canon',
            'type_of_photography': 'people',
            'social_media': 'linkedin',
            'website': 'www.test.com'
        }
        self.client.post(
            reverse('profile_edit', kwargs={'pk': self.user.pk}),
            data
        )
        # info after update
        attr = ['test', 'canon', 'people', 'linkedin', 'www.test.com']
        response = self.client.get(reverse('profile_view'))
        for x in attr:
            self.assertContains(response, x)
