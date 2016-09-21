from django.test import TestCase, Client
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User

# Create your tests here.


class ImagerProfileTest(TestCase):
    """Create test class for ImagerProfile model."""
    def setUp(self):
        """Set up a fake user and profile."""
        # import pdb; pdb.set_trace()
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


class Client():
    def test_client_response_code():
        """Test 200 response code received."""
        c = Client()
        response = c.post('/accounts/registration', {
            'username': 't',
            'email': 't@t.com',
            'password1': 'password',
            'password2': 'password'
            })
        assert response.status_code == 200

    def test_client_response_content():
        """Test content received upon successful registration."""
        c = Client()
        response = c.post('/accounts/registration', {
            'username': 't',
            'email': 't@t.com',
            'password1': 'password',
            'password2': 'password'
            })
        assert "The registration was successful check your email for activation link." in str(response.text)
