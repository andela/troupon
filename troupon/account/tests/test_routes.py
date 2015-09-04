# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.contrib.auth.models import User


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
        response = self.client.post('/auth/signin/',
                                    dict(email='johndoe@gmail.com',
                                         password='12345'))
        self.assertEquals(response.status_code, 302)
