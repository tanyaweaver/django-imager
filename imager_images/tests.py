from django.test import TestCase, override_settings
from imager_images.models import Photo
from django.contrib.auth.models import User
import os
from django.urls import reverse
from io import open
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PHOTO_PATH = os.path.join(HERE, 'test_resources', 'tree.jpg')
TEST_MEDIA_ROOT = tempfile.mkdtemp()


class PhotoAddTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test')
        self.user.set_password('supersecret')
        self.user.save()
        self.url = reverse('photo_add')
        self.tempdir = tempfile.mkdtemp()

    def TearDown(self):
        import shutil
        shutil.rmtree(self.tempdir)

    def get_auth_response(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        return response

    def test_add_photo_view_requires_auth(self):
        login_url = reverse('auth_login')
        response = self.client.get(self.url, follow=True)
        self.assertEquals(response.status_code, 200)
        chain = response.redirect_chain
        self.assertEqual(chain[0][1], 302)
        self.assertTrue(chain[0][0].startswith(login_url))

    def test_add_photo_availabale_to_auth(self):
        response = self.get_auth_response()
        self.assertEqual(response.status_code, 200)

    def test_form_present_in_context(self):
        response = self.get_auth_response()
        self.assertIn('form', response.context)

    def test_uploaded_photo_redirects_correctly(self):
        # with self.settings(MEDIA_ROOT=self.tempdir):
            # make sure there are no photos in db now
        self.assertEqual(Photo.objects.count(), 0)
        self.client.force_login(user=self.user)
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'photo': fh,
                'user': self.user.pk
            }
            response = self.client.post(self.url, data)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Photo.objects.count(), 1)
        new_photo = Photo.objects.first()
        self.assertEqual(new_photo.user, self.user)



class PhotoTest(TestCase):
    """Create test class for ImagerProfile model."""
    def setUp(self):
        """Set up a fake user and profile."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.photos = Photo(user=self.user)
        self.photos.save()

    def tearDown(self):
        """Delete fake user/profile after each test."""
        self.user.delete()
        self.photos.delete()

    def test_user_exists(self):
        """Prove the user exists."""
        self.assertTrue(self.user is not None)

    def test_photo_exists(self):
        """Prove that the user has a profile."""
        self.assertTrue(self.user.photos is not None)

    def test_profile_is_attached_to_right_user(self):
        """Prove that the profileis attached to the right user."""
        self.assertEqual(self.photos.user.username, 'test')
