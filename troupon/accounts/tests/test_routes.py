# -*- coding:utf-8 -*-
# All your tests for models used by the deals app go here

from django.test import TestCase, Client
from django.template.loader import render_to_string


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_route_accounts_profile(self):
        response = self.client.get('/accounts/profile/')
        self.assertEquals(response.status_code, 200)

    def test_route_accounts_settings(self):
        response = self.client.get('/accounts/settings/')
        self.assertEquals(response.status_code, 200)

    def test_route_accounts_history(self):
        response = self.client.get('/accounts/history/')
        self.assertEquals(response.status_code, 200)
