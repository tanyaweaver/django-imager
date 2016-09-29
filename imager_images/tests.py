from django.test import TestCase, override_settings
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
import os
from django.urls import reverse
from io import open
import tempfile
import factory

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PHOTO_PATH = os.path.join(HERE, 'test_resources', 'tree.jpg')
TEST_MEDIA_ROOT = tempfile.mkdtemp()


class EditAlbumTestCase(TestCase):
    """Define test case class for album editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.user = User(username='test')
        self.user.set_password('supersecret')
        self.user.save()
        self.album = Album(user=self.user)
        self.album.save()
        self.client.force_login(user=self.user)

    def tearDown(self):
        """Destroy setup."""
        self.user.delete()
        self.album.delete()

    def test_edit_album_button_url(self):
        """Prove that auth user has access to the edit."""
        url = reverse('album_edit', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_on_update_from_edit_album_page(self):
        """
        Prove that the user is redirected after successfully updating the
        an album.
        """
        url = reverse('album_edit', kwargs={'pk': 4})
        id_list = []
        photos = PhotoFactory.build_batch(10, user=self.user)
        for photo in photos:
            photo.save()
            id_list.append(photo.pk)
        data = {
            "photos": id_list
        }
        response = self.client.post(url, data)
        #import pdb; pdb.set_trace()
        self.assertEquals(response.status_code, 302)


class EditPhotoTestCase(TestCase):
    """Define test case class for photo editing."""
    def setUp(self):
        pass


class EditProfileTestCase(TestCase):
    """Define test case class for profile editing."""
    def setUp(self):
        pass

class PhotoFactory(factory.Factory):
    """Create a photo factory."""
    class Meta:
        model = Photo


class AlbumAddTestCAse(TestCase):
    """Define a class to test addition of album."""
    def setUp(self):
        """Set up our class."""
        self.user = User(username="test")
        self.user.set_password("supersecret")
        self.user.save()
        self.url = reverse('album_add')

    def tearDown(self):
        """Destroy setup."""
        self.user.delete()
        all_alb = Album.objects.all()
        all_alb.delete()

    def get_auth_response(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        return response

    def test_form_present_in_context(self):
        response = self.get_auth_response()
        self.assertIn('form', response.context)

    def test_add_album_redirects_correctly(self):
        self.assertEqual(Album.objects.count(), 0)
        self.client.force_login(user=self.user)
        ph = Photo(user=self.user)
        ph.save()
        data = {
            'photos': ph.pk
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Album.objects.count(), 1)
        new_photo = Photo.objects.first()
        self.assertEqual(new_photo.user, self.user)

    def test_album_has_correct_number_photos_added(self):
        """Test album adds correct number of photos."""
        self.client.force_login(user=self.user)
        id_list = []
        photos = PhotoFactory.build_batch(10, user=self.user)
        for photo in photos:
            photo.save()
            id_list.append(photo.pk)
        data = {
            "photos": id_list
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(Album.objects.filter(
            user=self.user).first().photos.count(), 10)


class PhotoAddTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test')
        self.user.set_password('supersecret')
        self.user.save()
        self.url = reverse('photo_add')
        self.tempdir = tempfile.mkdtemp()

    def TearDown(self):
        """Destroy setup."""
        # import shutil
        # shutil.rmtree(self.tempdir)
        self.user.delete()

    def get_auth_response(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        return response

    def test_form_present_in_context(self):
        response = self.get_auth_response()
        self.assertIn('form', response.context)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_uploaded_photo_redirects_correctly(self):
        self.assertEqual(Photo.objects.count(), 0)
        self.client.force_login(user=self.user)
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'photo': fh
            }
            response = self.client.post(self.url, data)
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
