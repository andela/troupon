import requests
import unittest

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from deals.models import Advertiser, Category, Deal
from merchant.models import Merchant
from ..models import Category, Deal, Advertiser, ALL_LOCATIONS


TEST_USER_EMAIL = 'testuser@myemail.com'
TEST_USER_PASSWORD = 'testpassword'
TEST_SEARCH_TERM = "Holiday"
TEST_SEARCH_LOCATION = "Nairobi"


class CreateDeal(object):

    def create_user(self):
        """Create the test user"""
        User.objects.create_user(username='mytestuser',
                                 email=TEST_USER_EMAIL,
                                 password=TEST_USER_PASSWORD)

    def create_user_profile(self):
        """Create the test user profile"""
        user_object = User.objects.all()[:1].get()
        user_profile = UserProfile.objects.create(
            user=user_object,
            occupation='Travel Agent',
            intlnumber='0705123456')
        return user_profile

    def create_merchant(self):
        """Create the test merchant"""
        merchant = Merchant.objects.create(
            userprofile=self.create_user_profile(),
            intlnumber='0705123456', enabled=True,
            approved=True, trusted=True)
        return merchant

    def get_location(self):
        """Returns mocked location of user"""
        ALL_LOCATIONS.insert(0, (999, 'Ashburn'))
        return 999

    def create_deal(self):
        """Create the test deal"""
        merchant = self.create_merchant()
        price = 5000
        original_price = 6000
        currency = 1
        country = 2
        location = self.get_location()
        quorum = 0
        disclaimer = ''
        description = 'Holiday for two to the luxurious Masai Mara.'
        title = 'Masai Mara Holiday'
        title2 = 'Beach holiday'
        address = 'Masai Mara'
        max_quantity_available = 20
        active = True
        advertiser_id = merchant.advertiser_ptr.id
        date_end = "2020-09-09"

        category = Category.objects.create(name="Travel N Hotels",
                                           slug="masai-mara-holiday")
        advertiser = Advertiser.objects.get(id=advertiser_id)

        deal = Deal(
            price=price, original_price=original_price, currency=currency,
            country=country, location=location, category=category,
            quorum=quorum, disclaimer=disclaimer, description=description,
            address=address, max_quantity_available=max_quantity_available,
            date_end=date_end, active=active, title=title,
            advertiser=advertiser, duration=20
        )

        deal.save()


class ServerAPITestCase(APITestCase, CreateDeal):

    def setUp(self):
        self.create_user()
        self.create_deal()

    def test_can_get_server_key(self):
        """Tests that server key can be obtained from environment"""
        response = self.client.get(
            "/api/serverkey/")
        self.assertEqual(response.status_code, 200)

    def test_filter_deals(self):
        """Tests that deals can be filtered according to location"""
        url = reverse('homepage')
        response = self.client.get(url)
        self.assertContains(response, 'Masai Mara Holiday')
