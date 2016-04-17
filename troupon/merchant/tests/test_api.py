"""Tests for deal management API endpoints."""
import json

from django.contrib.auth.models import User

from account.models import UserProfile
from deals.models import Deal, Category, Advertiser, Category
from merchant.api import DealListAPIView, DealActionsAPIView
from merchant.models import Merchant

from rest_framework.test import APITestCase


class DealAPITest(APITestCase):
    fixtures = ['deals.json']

    def test_unauthorized_access_is_not_allowed(self):
        response = self.client.get('/api/deals/')

        self.assertEqual(response.status_code, 403)
        detail = response.data.get('detail')
        self.assertIn('Authentication credentials were not provided.', detail)

    def test_merchant_can_access_all_his_deals(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.get('/api/deals/')

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(response.data.get('results'), {})
        self.assertEqual(response.data['count'], 1)

    def test_merchant_can_access_deal_by_id(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.get('/api/deals/21')

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data['title'], 'Fine Kenyan Coffee Beans')
        self.assertNotEqual(response.data.get('results'), {})

    def test_merchant_can_create_a_deal(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.post('/api/deals/',
                                    {
                                        'price': 300,
                                        'original_price': 500,
                                        'title': 'New deal',
                                        'max_quantity_available': 10,
                                        'category': 4,
                                        'description': 'New test deal',
                                        'quorum': 0
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 201)
        new_deal = response.data
        self.assertEqual(new_deal['title'], 'New deal')

    def test_merchant_can_update_deal(self):
        self.client.login(username="omondi", password="12345")
        update_data = {'title': 'New title'}

        update_response = self.client.patch('/api/deals/21', update_data)
        data = update_response.data

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(data['title'], 'New title')

    def test_merchant_can_delete_a_deal(self):
        self.client.login(username="omondi", password="12345")
        response = self.client.delete('/api/deals/21')

        self.assertEqual(204, response.status_code)
