# -*- coding:utf-8 -*-
# All your tests for models used by the deals app go here

from django.test import TestCase, Client
from django.template.loader import render_to_string


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_route_index(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_route_auth(self):
        response = self.client.get('/auth/')
        self.assertEquals(response.status_code, 200)
