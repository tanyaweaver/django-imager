from django.test import TestCase, override_settings
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
import os
from django.urls import reverse
from io import open
import factory
import tempfile
TEST_MEDIA_ROOT1 = tempfile.mkdtemp()

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PHOTO_PATH = os.path.join(HERE, 'test_resources', 'download.jpeg')


class PhotoModelTest(TestCase):
    """Create test class for Photo model."""
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


class PhotoFactory(factory.Factory):
    """Create a photo factory."""
    class Meta:
        model = Photo


class SetupTestCase(TestCase):
    """
    Define class for tests setup. All other test classes inherit
    form this class.
    """
    def setUp(self):
        """Define setup for tests.."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.tempdir = tempfile.mkdtemp()
        self.upload_2_photos_add_album()
        self.photo1 = self.user.photos.first()
        self.photo2 = self.user.photos.last()
        self.album = self.user.albums.all()[0]

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT1)
    def upload_2_photos_add_album(self):
        """Upload 2 photos and add 1 album for the user."""
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'user': self.user,
                'photo': fh,
                'description': 'my photo',
                'title': 'photo1'
            }
            self.client.post(reverse('photo_add'), data)
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'user': self.user,
                'photo': fh,
                'description': 'my photo',
                'title': 'photo 2'
            }
            self.client.post(reverse('photo_add'), data)
        ph = Photo.objects.filter(user=self.user).first()
        data = {
            'title': 'album1',
            'description': 'my album',
            'photos': ph.pk,
            'user': self.user,
        }
        self.client.post(reverse('album_add'), data)


class PhotosViewTestCase(SetupTestCase):
    """Define class to test photos view."""
    def setUp(self):
        self.setUp = super(PhotosViewTestCase, self).setUp()
        self.url = reverse('photos', kwargs={'pk': self.photo1.pk})
        self.response = self.client.get(self.url)
        self.template = 'imager_images/photo_page.html'

    def test_auth_user_has_access_to_photos(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render photos page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_photo_attributes_show_up(self):
        """Prove that all attributes show up on the page."""
        attr = [
            self.photo1.title,
            self.photo1.description,
            self.photo1.photo.url,
            ]
        for x in attr:
            self.assertContains(self.response, x)

    def test_published_status_in_context(self):
        """Prove that published status in context."""
        self.assertIn('status', self.response.context)


class AlbumsViewTestCase(SetupTestCase):
    """Define class to test albums view."""
    def setUp(self):
        """Define setup for tests."""
        self.setUp = super(AlbumsViewTestCase, self).setUp()
        self.url = reverse('albums', kwargs={'pk': self.album.pk})
        self.response = self.client.get(self.url)
        self.template = 'imager_images/album_page.html'

    def test_auth_user_has_access_to_albums(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render album page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_album_attributes_show_up(self):
        """Prove that all attributes show up on the page."""
        attr = [
            self.album.title,
            self.album.description,
            self.album.photos.all()[0].photo.url,
            self.album.photos.all()[0].is_cover,
            ]
        for x in attr:
            self.assertContains(self.response, x)

    def test_published_status_in_context(self):
        """Prove that published status in context."""
        self.assertIn('status', self.response.context)


class LibraryViewTestCase(SetupTestCase):
    """Define test class for libarry view."""
    def setUp(self):
        """Define setup for tests."""
        self.setUp = super(LibraryViewTestCase, self).setUp()
        self.url = reverse('library')
        self.response = self.client.get(self.url)
        self.template = 'imager_images/library_page.html'

    def test_auth_user_has_access_to_library(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render library page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_buttons_present(self):
        """Prove that expected buttons are present."""
        buttons = [
            reverse('album_add'),
            reverse('photo_add'),
            reverse('album_edit', kwargs={'pk': self.album.pk}),
            reverse('photo_edit', kwargs={'pk': self.photo1.pk}),
            reverse('photo_edit', kwargs={'pk': self.photo2.pk})
        ]
        for x in buttons:
            expected = 'href="{}"'.format(x)
            self.assertContains(self.response, expected)

    def test_albums_and_photos_in_context(self):
        """Prove that 'albums' and 'photos' are in response context."""
        list_ = ['albums', 'photos']
        for x in list_:
            self.assertIn(x, self.response.context)


class PhotoAddTestCase(SetupTestCase):
    """Set up class to test view for adding photos."""
    def setUp(self):
        """Define setup for tests."""
        self.setUp = super(PhotoAddTestCase, self).setUp()
        self.url = reverse('photo_add')
        self.response = self.client.get(self.url)
        self.template = 'imager_images/upload_photo_page.html'

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT1)
    def submit_photo(self):
        """Return response after submitting a photo."""
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'title': 'photo 3',
                'description': 'another photo',
                'photo': fh,
            }
            response = self.client.post(self.url, data)
        return response

    def test_auth_user_has_access_to_add_photo(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_right_template_is_used(self):
        """Prove that right template is used to render add photo page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_uploaded_photo_added_correctly(self):
        """Prove that 1 photo is added to the db after photo upload."""
        # there are 2 photos in the db already (see SetupTestCase setUp(self))
        self.assertEqual(self.user.photos.all().count(), 2)
        self.submit_photo()
        self.assertEqual(self.user.photos.all().count(), 3)

    def test_uploaded_photo_has_right_attributes(self):
        """
        Prove that the new photo is associated with the correct user and has
        correct title and description.
        """
        self.submit_photo()
        new_photo = Photo.objects.last()
        self.assertEqual(new_photo.user, self.user)
        self.assertEqual(new_photo.title, 'photo 3')
        self.assertEqual(new_photo.description, 'another photo')

    def test_redirection_after_photo_submitted(self):
        """Prove redirection to library page after uploading a photo."""
        response = self.submit_photo()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/images/library/')


class AlbumAddTestCase(SetupTestCase):
    """Define a class to test addition of album."""
    def setUp(self):
        """Set up the class."""
        self.setUp = super(AlbumAddTestCase, self).setUp()
        self.url = reverse('album_add')
        self.response = self.client.get(self.url)
        self.template = 'imager_images/add_album_page.html'

    def add_album(self):
        """Return response after submitting an album with 10 photos."""
        id_list = []
        photos = PhotoFactory.build_batch(10, user=self.user)
        for photo in photos:
            photo.save()
            id_list.append(photo.pk)
        data = {
            "title": 'album 2',
            "description": "another album",
            "photos": id_list
        }
        response = self.client.post(self.url, data)
        return response

    def test_auth_user_has_access_to_add_album(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render add album page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_add_album_correctly(self):
        """
        Prove that 1 album is added to the db after submit.
        Prove that the album is associated with the correct user.
        """
        # there is 1 album in the db already (see SetupTestCase setUp(self))
        self.assertEqual(self.user.albums.all().count(), 1)
        self.add_album()
        self.assertEqual(self.user.albums.all().count(), 2)

    def test_added_album_has_right_attributes(self):
        """
        Prove that the new album is associated with the correct user and has
        correct title and description.
        """
        self.add_album()
        new_album = Album.objects.last()
        self.assertEqual(new_album.user, self.user)
        self.assertEqual(new_album.title, 'album 2')
        self.assertEqual(new_album.description, 'another album')

    def test_album_has_correct_number_photos_added(self):
        """Test album adds correct number of photos."""
        self.add_album()
        self.assertEqual(Album.objects.filter(
            user=self.user).last().photos.count(), 10)

    def test_add_album_redirects_correctly(self):
        """Prove redirection to library page after adding an album."""
        response = self.add_album()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/images/library/')


class EditPhotoTestCase(SetupTestCase):
    """Define test case class for photo editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.setUp = super(EditPhotoTestCase, self).setUp()
        self.url = reverse('photo_edit', kwargs={'pk': self.photo1.pk})
        self.response = self.client.get(self.url)
        self.template = 'imager_images/edit_photo_page.html'
        self.data = {
                'title': 'photo1 updated',
                'description': 'my photo updated'
                }

    def test_auth_user_have_access_to_photo_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit photo page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_photo_update(self):
        """Prove redirection to the library page after photo edited."""
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/images/library/')

    def test_photo_info_updated(self):
        """Prove that photo info was updated."""
        self.assertEquals(self.photo1.title, 'photo1')
        self.assertEquals(self.photo1.description, 'my photo')
        self.client.post(self.url, self.data)
        photo = Photo.objects.filter(user=self.user).first()
        self.assertEqual(photo.title, 'photo1 updated')
        self.assertEqual(photo.description, 'my photo updated')

    def test_number_of_photos_didnt_change(self):
        """
        Prove that after updating a photo, the total number of photos
        didn't change.
        """
        # number of photos before update
        count1 = Photo.objects.filter(user=self.user).all().count()
        self.client.post(self.url, self.data)
        # number of photos after update
        count2 = Photo.objects.filter(user=self.user).all().count()
        self.assertEqual(count1, count2)


class EditAlbumTestCase(SetupTestCase):
    """Define test case class for album editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.setUp = super(EditAlbumTestCase, self).setUp()
        self.url = reverse('album_edit', kwargs={'pk': self.album.pk})
        self.response = self.client.get(self.url)
        self.template = 'imager_images/edit_album_page.html'
        self.data = {
            "title": 'album1 updated',
            "description": " my album updated",
            "photos": self.photo2.pk
        }

    def test_auth_user_have_access_to_album_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit album page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_update_from_edit_album_page(self):
        """Prove redirection to library page after updating an album."""
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/images/library/')

    def test_album_info_updated(self):
        """Prove that album info was updated."""
        self.assertEqual(self.album.title, 'album1')
        self.assertEqual(self.album.description, 'my album')
        self.assertEqual(self.album.photos.first().pk, self.photo1.pk)
        self.client.post(self.url, self.data)
        album = Album.objects.filter(user=self.user).first()
        self.assertEqual(album.title, 'album1 updated')
        self.assertEqual(album.description, 'my album updated')
        self.assertEqual(self.album.photos.first().pk, self.photo2.pk)

    def test_number_of_albums_didnt_change(self):
        """
        Prove that after updating a album, the total number of albums
        didn't change.
        """
        # number of albums before update
        count1 = self.user.albums.all().count()
        self.client.post(self.url, self.data)
        # number of albums after update
        count2 = self.user.albums.all().count()
        self.assertEqual(count1, count2)

    def test_number_of_photos_in_album_didnt_change(self):
        """
        Prove that after updating a album, the total number of photos
        in that album didn't change.
        """
        # number of photos before update
        count1 = self.user.albums.first().photos.all().count()
        self.client.post(self.url, self.data)
        # number of photos after update
        count2 = self.user.albums.first().photos.all().count()
        self.assertEqual(count1, count2)
