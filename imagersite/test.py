from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
import factory
from imager_profile.models import ImagerProfile


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


class LoginTest(TestCase):
    """Create Login test case."""
    def setUp(self):
        """Set up response for login tests."""
        self.user = UserFactory()
        self.user.username = 'bob'
        self.user.set_password('sldkfje837&')
        self.user.save()

    def tearDown(self):
        """Tear down set up."""
        pass

    def test_login_successful_redirection(self):
        """Test successful login redirection."""
        self.response = self.client.get(reverse('homepage'))
        self.assertEqual(self.response.status_code, 200)

    def test_auth_user_homepage_view(self):
        """Test homepage has 'welcome username'."""
        self.response = self.client.post(reverse('auth_login'), {
            "username": 'bob', "password": "sldkfje837&"})
        # self.response = self.client.get(reverse('homepage'))
        # import pdb; pdb.set_trace()
        self.assertEqual(self.response.status_code, 302)
