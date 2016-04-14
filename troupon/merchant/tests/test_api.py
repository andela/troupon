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
        username = User.objects.get().username
        password = "12345"

        self.client.login(username="omondi", password="12345")

    def test_merchant_can_access_all_his_deals(self):
        response = self.client.get('/api/deals/')

        self.assertEqual(response.status_code, 200)
