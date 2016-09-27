from django.test import TestCase
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
from django.urls import reverse
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User


class ProfileTestCase(TestCase):
    """Define test class for Profile View."""
    def setUp(self):
        self.profile_url = reverse('profile_view')
        self.user = UserFactory().create()

    def test_anon_user_is_redirected_to_login1(self):
        response = self.client.get(self.profile_url, follow=True)
        login_url = reverse('auth_login')
        expected_url = '{}?{}'.format(login_url, self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[1], 302)
        self.assertTupleEqual(response.redirect_chain[0], expected_url)

    def test_auth_user_can_get_profile(self):
        response = self.client.get(self.profile_url)
        self.client.force_login(user=self.user)
        self.assertEquals(response.status_code, 200)




# class ImagerProfileTestCase(TestCase):
#     """Create test class for ImagerProfile model."""
#     def setUp(self):
#         """Set up a fake user and profile."""
#         self.user = User(username='test')
#         self.user.set_password('test')
#         self.user.save()
#
#     def tearDown(self):
#         """Delete fake user/profile after each test."""
#         self.user.delete()
#         self.user.profile.delete()
#
#     def test_user_exists(self):
#         """Prove the user exists."""
#         self.assertTrue(self.user is not None)
#
#     def test_username(self):
#         """Prove the username is correct."""
#         self.assertEqual(self.user.username, 'test', 'wrong username')
#
#     def test_profile_exists(self):
#         """Prove that the user has a profile."""
#         self.assertTrue(self.user.profile is not None)
#
#     def test_profile_is_attached_to_right_user(self):
#         """Prove that the profileis attached to the right user."""
#         self.assertEqual(self.user.profile.user.username, 'test')
