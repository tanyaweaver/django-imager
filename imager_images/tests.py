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


class PhotoModelTest(TestCase):
    """Create test class for Photo model."""
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUp(self):
        """Set up a fake user and photo."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.photo = Photo(user=self.user)
        self.photo.save()
        self.album = Album(user=self.user)
        self.album.save()
        self.photo.albums.add(self.album)

    def test_photo_exists(self):
        """Prove that the user has one photo."""
        self.assertEquals(self.user.photos.count(), 1)

    def test_photo_is_attached_to_right_user(self):
        """Prove that the photo is attached to the right user."""
        self.assertEqual(self.photo.user.username, 'test')

    def test_photo_is_not_a_cover_by_default(self):
        """Prove that the photo is not a cover by default."""
        self.assertEqual(self.photo.is_cover, False)

    def test_photo_belongs_to_album(self):
        """Prove that the photo belongs_to_album."""
        self.assertEqual(self.photo.albums.count(), 1)


class AlbumModelTest(TestCase):
    """Create test class for Album model."""
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUp(self):
        """Set up a fake user and photo."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.photo = Photo(user=self.user)
        self.photo.save()
        self.album = Album(user=self.user)
        self.album.save()
        self.photo.albums.add(self.album)

    def test_album_exists(self):
        """Prove that the user has one album."""
        self.assertEquals(self.user.albums.count(), 1)

    def test_album_is_attached_to_right_user(self):
        """Prove that the album is attached to the right user."""
        self.assertEqual(self.album.user.username, 'test')

    def test_album_does_not_have_a_cover_by_default(self):
        """Prove that an album does not have a cover by default."""
        self.assertEqual(self.album.cover, None)

    def test_album_has_one_photo(self):
        """Prove that the album has 1 photo in it"""
        self.assertEqual(self.album.photos.count(), 1)


class PhotosViewTestCase(TestCase):
    """Define class to test photos view."""
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.tempdir = tempfile.mkdtemp()
        self.upload_photos_add_album()
        self.photo = Photo.objects.filter(user=self.user).first()
        self.album = Album.objects.filter(user=self.user).first()
        self.url = reverse('photos', kwargs={'pk': self.photo.pk})
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

    def test_auth_user_has_access_to_photos(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render photos page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/photo_page.html'
        )


class AlbumsViewTestCase(TestCase):
    """Define class to test albums view."""
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.tempdir = tempfile.mkdtemp()
        self.upload_photos_add_album()
        self.photo = Photo.objects.filter(user=self.user).first()
        self.album = Album.objects.filter(user=self.user).first()
        self.url = reverse('albums', kwargs={'pk': self.album.pk})
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

    def test_auth_user_has_access_to_albums(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render album page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/album_page.html'
        )


class PhotoFactory(factory.Factory):
    """Create a photo factory."""
    class Meta:
        model = Photo


class LibraryViewTestCase(TestCase):
    """Define test class for libarry view."""
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.tempdir = tempfile.mkdtemp()
        self.upload_photos_add_album()
        self.photo = Photo.objects.filter(user=self.user).first()
        self.album = Album.objects.filter(user=self.user).first()
        self.url = reverse('library')
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

    def test_auth_user_has_access_to_library(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render library page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/library_page.html'
        )

    def test_buttons_present(self):
        """Prove that expected buttons are present."""
        buttons = [
            reverse('album_add'),
            reverse('photo_add'),
            reverse('album_edit', kwargs={'pk': self.album.pk}),
            reverse('photo_edit', kwargs={'pk': self.photo.pk})
        ]
        for x in buttons:
            expected = 'href="{}"'.format(x)
            self.assertContains(self.response, expected)

    def test_albums_and_photos_in_context(self):
        """Prove that 'albums' and 'photos' are in response context."""
        list_ = ['albums', 'photos']
        for x in list_:
            self.assertIn(x, self.response.context)


class PhotoAddTestCase(TestCase):
    """Set up class to test view for adding photos."""
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.url = reverse('photo_add')
        self.response = self.client.get(self.url)
        self.tempdir = tempfile.mkdtemp()

    def test_auth_user_has_access_to_add_photo(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_right_template_is_used(self):
        """Prove that right template is used to render add photo page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/upload_photo_page.html'
        )

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def submit_photo(self):
        """Return response after submitting a photo."""
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'photo': fh
            }
            response = self.client.post(self.url, data)
        return response

    def test_uploaded_photo_added_correctly(self):
        """
        Prove that 1 photo is added to the db after photo upload. Prove that
        the photo is associated with the correct user.
        """
        self.assertEqual(Photo.objects.count(), 0)
        self.submit_photo()
        self.assertEqual(Photo.objects.count(), 1)
        new_photo = Photo.objects.first()
        self.assertEqual(new_photo.user, self.user)

    def test_redirection_after_photo_submitted(self):
        """
        Prove redirection to the library page after uploading a photo.
        """
        response = self.submit_photo()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/images/library/')


class AlbumAddTestCAse(TestCase):
    """Define a class to test addition of album."""
    def setUp(self):
        """Set up the class."""
        self.user = User(username="test")
        self.user.set_password("supersecret")
        self.user.save()
        self.url = reverse('album_add')
        self.client.force_login(user=self.user)
        self.response = self.client.get(self.url)

    def test_auth_user_has_access_to_add_album(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render add album page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/add_album_page.html'
        )

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def submit_album(self):
        """Return response after submitting an album."""
        ph = Photo(user=self.user)
        ph.save()
        data = {
            'photos': ph.pk
        }
        response = self.client.post(self.url, data)
        return response

    def test_add_album_correctly(self):
        """
        Prove that 1 album is added to the db after submit.
        Prove that the album is associated with the correct user.
        """
        self.assertEqual(Album.objects.count(), 0)
        self.submit_album()
        self.assertEqual(Album.objects.count(), 1)
        new_photo = Photo.objects.first()
        self.assertEqual(new_photo.user, self.user)

    def test_add_album_redirects_correctly(self):
        """
        Prove redirection to the library page after adding an album.
        """
        response = self.submit_album()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/images/library/')

    def test_album_has_correct_number_photos_added(self):
        """Test album adds correct number of photos."""
        id_list = []
        photos = PhotoFactory.build_batch(10, user=self.user)
        for photo in photos:
            photo.save()
            id_list.append(photo.pk)
        data = {
            "photos": id_list
        }
        self.client.post(self.url, data)
        self.assertEqual(Album.objects.filter(
            user=self.user).first().photos.count(), 10)


class EditPhotoTestCase(TestCase):
    """Define test case class for photo editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.user = User(username='test')
        self.user.set_password('supersecret')
        self.user.save()
        self.photo = Photo(user=self.user)
        self.photo.save()
        self.client.force_login(user=self.user)
        self.url = reverse('photo_edit', kwargs={'pk': self.photo.pk})
        self.response = self.client.get(self.url)

    def test_auth_user_have_access_to_photo_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit photo page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/edit_photo_page.html'
        )

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_photo_update(self):
        """
        Prove redirection to the library page after photo edited.
        """
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/images/library/')


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
        self.url = reverse('album_edit', kwargs={'pk': self.album.pk})
        self.response = self.client.get(self.url)

    def photos_to_submit(self):
        """Create photos to submit with post request."""
        id_list = []
        photos = PhotoFactory.build_batch(10, user=self.user)
        for photo in photos:
            photo.save()
            id_list.append(photo.pk)
        data = {
            "photos": id_list
        }
        return data

    def test_auth_user_have_access_to_album_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit album page."""
        self.assertTemplateUsed(
            self.response,
            'imager_images/edit_album_page.html'
        )

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_update_from_edit_album_page(self):
        """
        Prove redirection to the library page after successfully updating
        an album.
        """
        data = self.photos_to_submit()
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/images/library/')

    def test_album_has_right_number_photos_added(self):
        """Test album adds correct number of photos."""
        data = self.photos_to_submit()
        self.client.post(self.url, data)
        self.assertEqual(Album.objects.filter(
            user=self.user).first().photos.count(), 10)
