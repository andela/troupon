"""Tests for deal management API endpoints."""
import json

from django.contrib.auth.models import User
from django.test import TestCase

from account.models import UserProfile
from deals.models import Deal, Category, Advertiser, Category
from merchant.api import DealListAPIView, DealActionsAPIView
from merchant.models import Merchant

from rest_framework.test import APITestCase


class DealAPITest(TestCase):
    fixtures = ['deals.json']

    def setUp(self):
        username = User.objects.first().username

        password = "12345"

        self.client.login(username="omondi", password="12345")

    def test_merchant_can_access_all_his_deals(self):
        response = self.client.get('/api/deals/')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.data.get('results'), {})
        self.assertEqual(response.data['count'], 1)

    def test_merchant_can_access_deal_by_id(self):
        response = self.client.get('/api/deals/21')

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['title'], 'Fine Kenyan Coffee Beans')
        self.assertNotEqual(response.data.get('results'), {})
