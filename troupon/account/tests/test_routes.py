# -*- coding: utf-8 -*-

from django.test import TestCase, Client
<<<<<<< HEAD
<<<<<<< HEAD
from django.contrib.auth.models import User
from account.views import ForgotPasswordView, ResetPasswordView
=======
from account.views import ForgotPasswordView, ResetFromEmailView
>>>>>>> [#102569504] Feature-Forgot-Password: implemented 'reset_from_email' route

class UserSigninTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User(username='johndoe@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def test_route_get_auth_signin(self):
        response = self.client.get('/auth/signin/')
        self.assertEquals(response.status_code, 200)

    def test_route_post_auth_signin(self):
        response = self.client.post('/auth/signin/', dict(email='johndoe@gmail.com', password='12345'))
        self.assertEquals(response.status_code, 302)



class ForgotRecoverPasswordRoutesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_forgot_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/')
        self.assertEqual(response.resolver_match.func.__name__, ForgotPasswordView.as_view().__name__)

    def test_reset_route_resolves_to_correct_view(self):
        response = self.client.get('/account/recovery/ajkzfYba9847DgJ7wbkwAaSbkTjUdawGG998qo3HG8qae83')
        self.assertEqual(response.resolver_match.func.__name__, ResetPasswordView.as_view().__name__)
