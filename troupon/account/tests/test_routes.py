# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.core.context_processors import csrf
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from account.views import ForgotPasswordView, ResetPasswordView
from allaccess.views import OAuthRedirect,OAuthCallback

from mock import patch


class UserSigninTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User(username='johndoe@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_route_get_auth_signin(self):
        response = self.client.get('/account/signin/')
        self.assertEquals(response.status_code, 200)

    def test_route_post_auth_signin(self):
        response = self.client.post('/account/signin/',
                                    dict(email='johndoe@gmail.com',
                                         password='12345'))
        self.assertEquals(response.status_code, 302)


class ForgotPasswordRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_forgot_route_returns_200(self):
        response = self.client.get('/account/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_post_forgot_route_returns_200(self):
        response = self.client.post('/account/recovery/', {"email": "random@mail.com"})
        self.assertEquals(response.status_code, 200)

    def test_forgot_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/')
        self.assertEqual(response.resolver_match.func.__name__, ForgotPasswordView.as_view().__name__)


class ResetPasswordRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_reset_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/ajkzfYba9847DgJ7wbkwAaSbkTjUdawGG998qo3HG8qae83')
        self.assertEqual(response.resolver_match.func.__name__, ResetPasswordView.as_view().__name__)


class UserRegistrationViewTest(TestCase):
  '''
  Test class to user registration.
  '''
  def setUp(self):
    '''
    User sign's up with data.
    '''
    self.client_stub = Client()
    self.form_data = dict(username="andela",
                           password1="andela",
                           password2="andela",
                           email="andela@andela.com",
                           )

  def test_view_signup_route(self):
    '''
    User signup page is called.
    '''

    response = self.client_stub.get('/account/signup/')
    self.assertEquals(response.status_code, 200)

  def test_view_reg_route(self):
    '''
    User is redirected after signup data is validated.
    '''
    response = self.client_stub.post('/account/signup/', self.form_data)
    self.assertEquals(response.status_code, 302)

  def test_view_reg_success_route(self):
    '''
    User gets to view confirmation page after signup.
    '''

    response = self.client_stub.get('/account/confirm/')
    self.assertEquals(response.status_code, 200)


class UserSignInViewTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User(username='johndoe@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_view_get_auth_signin(self):
        """Test that user request for signin page binds to a view called
            the class name `UserSigninView`.
        """

        response = resolve('/account/signin/')
        self.assertEquals(response.func.__name__, 'UserSigninView')

    def test_view_post_auth_signin(self):
        """Test that user post to signin route has a session
        """
        data = {'email': 'johndoe@gmail.com', 'password': '12345'}
        response = self.client.post('/account/signin/', data)
        self.assertIn('deals', response.content)

class FacebookSignupTestCase(TestCase):

    def setUp(self):
        self.client_stub = Client()


    def test_user_signup_via_facebook(self):
        response = self.client_stub.post('/accounts/login/facebook/')
        self.assertEqual(response.resolver_match.func.__name__, OAuthRedirect.as_view().__name__)

       
    def test_user_redirected_after_facebook_signup(self):
        response = self.client_stub.post('/accounts/callback/facebook/')
        self.assertEqual(response.resolver_match.func.__name__, OAuthCallback.as_view().__name__)



