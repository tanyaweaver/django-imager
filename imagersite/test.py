from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
import factory
from imager_images.models import Photo, Album


class HomePageTestCase(TestCase):
    """Create Home Page test case."""

    def setUp(self):
        """Set up response for home page test case."""
        self.response = self.client.get(reverse("homepage"))

    def tearDown(self):
        """Tear down setup."""
        pass

    def test_for_registration_button(self):
        """Prove response contains registration page link."""
        reg_url = reverse("registration_register")
        expected = 'href="{}"'.format(reg_url)
        self.assertContains(self.response, expected, status_code=200)

    def test_for_login_button(self):
        """Assert that the response contains a link to the login page"""
        login_url = reverse('auth_login')
        expected = 'href="{}"'.format(login_url)
        self.assertContains(self.response, expected, status_code=200)

    def test_home_page_uses_right_template(self):
        """Assert that the home page view is rendered with our view."""
        for template_name in [
            'imagersite/home.html', 'imagersite/base.html'
        ]:
            self.assertTemplateUsed(self.response, template_name)

    def test_home_page_context_contains_coverpath(self):
        """Assert that the context used to render the home page is right."""
        self.assertTrue('cover_path' in self.response.context)


class RegistrationTestCase(TestCase):
    """Setup Registration test case."""
    def setUp(self):
        """Set up response for registration test case."""
        self.response = self.client.post('/accounts/register/', {
            'username': 't',
            'email': 't@t.com',
            'password1': 'fseIJE#*$83',
            'password2': 'fseIJE#*$83'
            })

    def tearDown(self):
        """Tear down setup."""
        pass

    def test_client_response_code(self):
        """Test 302 response code received."""
        self.assertEqual(self.response.status_code, 302)

    def test_client_response_content(self):
        """Test content received upon successful registration."""
        self.assertEqual(self.response.url, "/accounts/register/complete/")

    def test_registration_complete_page_uses_right_template(self):
        """Assert that registration page view is rendered with our template."""
        for template_name in [
            "registration/activation_email_subject.txt",
            "registration/activation_email.txt"
        ]:
            self.assertTemplateUsed(self.response, template_name)


class EmailTest(TestCase):
    """Set up Email Test Class."""
    def test_send_email(self):
        """Tests that registration email was sent."""
        mail.send_mail(
            "Registration details", "This is the registration message.",
            'user@djangoimager.com', ['s@s.com', 'd@s.com'],
            fail_silently=False,
        )
        # Tests that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the subject of the first message is as expected
        self.assertEqual(mail.outbox[0].subject, "Registration details")

        # Verify the message of the email is as expected
        self.assertEqual(
            mail.outbox[0].message()._payload,
            "This is the registration message.")

        # Verify the recipients are as expected
        self.assertEqual(mail.outbox[0].to, ['s@s.com', 'd@s.com'])

        # Verify the sender is as expected
        self.assertEqual(mail.outbox[0].from_email, "user@djangoimager.com")


class UserFactory(factory.Factory):
    class Meta:
        model = User


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album


class AuthTest(TestCase):
    """Create Login test case."""
    def setUp(self):
        """Set up response for login tests."""
        self.user = UserFactory()
        self.user.username = 'bob'
        self.user.set_password('sldkfje837&')
        self.user.save()
        self.login_response = self.client.post(
            reverse('auth_login'),
            {"username": 'bob', "password": "sldkfje837&"}
        )
        self.profile_login_response = self.client.get(reverse('profile_view'))
        self.logout_response = self.client.get(reverse('auth_logout'))
        self.home_logout_response = self.client.get(reverse('homepage'))

    def test_login_successful_redirection(self):
        """Test successful login redirection."""
        self.assertEqual(self.login_response.status_code, 302)

    def test_auth_user_profile_page_view(self):
        """Test profile page has 'Welcome, <username>'."""
        self.assertContains(self.profile_login_response, "Welcome, bob")

    def test_welcome_username_linked_to_profile_page(self):
        """Test that 'Welcome, <username>' links to profile page."""
        profile_url = reverse('profile_view')
        expected = 'href="{}"'.format(profile_url)
        self.assertContains(self.profile_login_response, expected)

    def test_logout_button_exists(self):
        """Test auth user has logout button on profile page and right url."""
        logout_url = reverse('auth_logout')
        expected = 'href="{}"'.format(logout_url)
        self.assertContains(self.profile_login_response, expected)

    def test_library_button_exists(self):
        """Test auth user has library button on profile page and right url."""
        library_url = reverse('library')
        expected = 'href="{}"'.format(library_url)
        self.assertContains(self.profile_login_response, expected)

    def test_logout_succesful_redirection(self):
        """Test successful logout redirection."""
        self.assertEqual(self.logout_response.status_code, 302)

    def test_unauth_user_homepage_view(self):
        """Test homepage has no 'Welcome, username' if unauth."""
        self.assertNotContains(self.home_logout_response, "Welcome, bob")

    def test_no_logout_button_if_unauth(self):
        """Test auth user has no logout button on homepage if unauth."""
        logout_url = reverse('auth_logout')
        expected = 'href="{}"'.format(logout_url)
        self.assertNotContains(self.home_logout_response, expected)


class UrlAccessTestCase(TestCase):
    """Define test class for url access."""
    def setUp(self):
        """Setup for the class."""
        self.user = User(username='test')
        self.user.save()
        self.album = Album(user=self.user)
        self.album.save()
        self.photo = Photo(user=self.user)
        self.photo.save()

    def submit_photo(self):
        """Return response after submitting a photo."""
        with open(TEST_PHOTO_PATH, 'rb') as fh:
            data = {
                'photo': fh
            }
            response = self.client.post(reverse('photo_add'), data)
        return response

    def test_anon_user_is_redirected_to_login_from_all_urls(self):
        """Prove that an unauth user is redirected to login."""
        urls = [
            reverse('profile_view'),
            reverse('library'),
            reverse('photos', kwargs={'pk': self.user.pk}),
            reverse('albums', kwargs={'pk': self.user.pk}),
            reverse('album_add'),
            reverse('photo_add'),
            reverse('photo_edit', kwargs={'pk': self.photo.pk}),
            reverse('album_edit', kwargs={'pk': self.album.pk}),
            reverse('profile_edit', kwargs={'pk': self.user.pk})
            ]
        for url in urls:
            response = self.client.get(url, follow=True)
            login_url = reverse('auth_login')
            expected_url = '{}?next={}'.format(login_url, url)
            expected = (expected_url, 302)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertTupleEqual(response.redirect_chain[0], expected)

    def test_auth_user_have_access_to_urls(self):
        """
        Prove that an auth user has access to '/profile/', '/library/',
        '/photos/', '/albums/'.
        """
        self.client.force_login(user=self.user)
        urls = [
            reverse('profile_view'),
            # reverse('library'),
            # reverse('photos', kwargs={'pk': self.photo.pk}),
            reverse('albums', kwargs={'pk': self.album.pk}),
            ]
        for url in urls:
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
