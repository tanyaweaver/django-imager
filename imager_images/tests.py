from django.test import TestCase
from imager_images.models import Photo
from django.contrib.auth.models import User


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
