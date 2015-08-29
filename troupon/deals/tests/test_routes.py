# -*- coding:utf-8 -*-
# All your tests for models used by the deals app go here

from django.test import TestCase, Client
from django.template.loader import render_to_string
from deals import views


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_route_signup(self):
        response = self.client.get('/auth/')
        self.assertEquals(response.status_code, 200)