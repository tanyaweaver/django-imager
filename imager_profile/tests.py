from django.test import TestCase
from django.contrib.auth.models import User
# from imager_profile.models import ImagerProfile
# from django.urls import reverse
# import factory


class ImagerProfileTestCase(TestCase):
    """Create test class for ImagerProfile model."""
    def setUp(self):
        """Set up a fake user and profile."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()

    def tearDown(self):
        """Delete fake user/profile after each test."""
        self.user.delete()
        self.user.profile.delete()

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
