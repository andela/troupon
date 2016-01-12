# -*- coding: utf-8 -*-
from mock import patch

from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

from allaccess.views import OAuthRedirect, OAuthCallback

from authentication.views import ForgotPasswordView, ResetPasswordView,\
    ActivateAccountView
from authentication.emails import SendGrid


class UserLoginRouteTestCase(TestCase):
    """
    Test that post and get requests to login routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_route_get_auth_login(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

    def test_route_post_auth_login(self):
        response = self.client.post('/login/',
                                    dict(username='johndoe@gmail.com',
                                         password='12345'))
        self.assertEquals(response.status_code, 302)


class UserLogoutRouteTestCase(TestCase):
    """
    Test that user can logout of session.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_route_get_auth_logout(self):
        self.client.post(
            '/login',
            dict(
                username='johndoe@gmail.com',
                password='12345'
            )
        )
        response = self.client.get('/logout/')
        self.assertIsNone(response.context)
        self.assertEquals(response.status_code, 302)


class ForgotPasswordRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_forgot_route_returns_200(self):
        response = self.client.get('/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_post_forgot_route_returns_200(self):
        response = self.client.post(
            '/recovery/',
            {"email": "random@mail.com"}
        )
        self.assertEquals(response.status_code, 200)

    def test_forgot_route_resolves_to_correct_view(self):
        response = self.client.get('/recovery/')
        self.assertEqual(
            response.resolver_match.func.__name__,
            ForgotPasswordView.as_view().__name__
        )


class ResetPasswordRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_reset_route_resolves_to_correct_view(self):
        response = self.client.get(
            '/recovery/ajkzfYba9847DgJ7wbkwAaSbkTjUdawGG998qo3HG8qae83'
        )
        self.assertEqual(
            response.resolver_match.func.__name__,
            ResetPasswordView.as_view().__name__
        )


class UserRegistrationRouteTest(TestCase):
    """
    Test class to user registration.
    """

    def setUp(self):
        """
        User sign's up with data.
        """
        self.client_stub = Client()

        self.form_data = dict(
            username="andela",
            password1="andela",
            password2="andela",
            email="andela@andela.com",
        )

    def test_view_register_route(self):
        """
        User register page is called.
        """
        response = self.client_stub.get('/register/')
        self.assertEquals(response.status_code, 200)

    def test_view_reg_route(self):
        """
        User is redirected after registration data is validated.
        """
        with patch.object(SendGrid, 'send', return_value=200) \
                as mock_method:
                response = self.client_stub.post(
                    '/register/',
                    self.form_data)
                self.assertEquals(response.status_code, 302)

    def test_view_reg_success_route(self):
        """
        User gets to view confirmation page after registration.
        """
        response = self.client_stub.get('/confirm/')
        self.assertEquals(response.status_code, 200)

    def test_user_register_function_called(self):
        """
        Test that register route binds to UserRegistrationView
        """
        response = resolve('/register/')
        self.assertEquals(response.func.__name__, 'UserRegistrationView')


class FacebookSignupTestCase(TestCase):

    def setUp(self):
        self.client_stub = Client()

    def test_user_signup_via_facebook(self):
        response = self.client_stub.post('/accounts/login/facebook/')
        self.assertEqual(
            response.resolver_match.func.__name__,
            OAuthRedirect.as_view().__name__
        )

    def test_user_redirected_after_facebook_signup(self):
        response = self.client_stub.post('/accounts/callback/facebook/')
        self.assertEqual(
            response.resolver_match.func.__name__,
            OAuthCallback.as_view().__name__
        )


class ActivateAccountRoute(TestCase):

    def Setup(self):
        self.client_stub = Client()

    def test_activation_link_calls_actual_view_class(self):
        response = self.client.get(
            '/activation/ajkzfYba9847DgJ7wbkwAaSbkTjUdawGG998qo3HG8qae83'
        )
        self.assertEqual(
            response.resolver_match.func.__name__,
            ActivateAccountView.as_view().__name__
        )
