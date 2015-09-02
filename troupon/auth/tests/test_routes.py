# -*- coding: utf-8 -*-

from django.test import TestCase, Client


class AuthentationSignInTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """
    
    def setUp(self):
        self.client = Client()

    def test_route_get_auth_signin(self):
        response = self.client.get('/auth/signin')
        self.assertEquals(response.status_code, 200)

    def test_route_post_auth_signin(self):
        response = self.client.post('/auth/signin')
        self.assertEquals(response.status_code, 200)

