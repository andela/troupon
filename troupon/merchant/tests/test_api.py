"""Tests for deal management API endpoints."""
from django.contrib.auth.models import User

from account.models import UserProfile
from deals.models import Deal, Category, Advertiser, Category
from merchant.api import DealListAPIView, DealActionsAPIView
from merchant.models import Merchant

from rest_framework.test import APITestCase


def create_test_user():
    user = User.objects.create_user(username="amos",
                                    email="amos@test.com",
                                    password="12345")
    return user


def create_merchant(user):
    user_profile = UserProfile.objects.create(user=user,
                                              user_state=25,
                                              occupation='Software Developer',
                                              intlnumber='0712456271')

    merchant = Merchant.objects.create(userprofile=user_profile,
                                       intlnumber='0712456271',
                                       enabled=True,
                                       approved=True,
                                       trusted=True)

    return merchant


def create_deal(merchant):
    merchant = merchant
    price = 800
    original_price = 1200
    currency = 1
    state = 25
    quorum = 0
    disclaimer = 'None'
    description = 'Awesome sofa set'
    title = 'Sofa'
    address = '525 Kindaruma Road, Kilimani, Nairobi'
    max_quantity_available = 200
    active = True
    advertiser_id = merchant.advertiser_ptr.id
    date_end = "2015-03-03"
    category = Category.objects.create(name="Electronics", slug="stuff")
    advertiser = Advertiser.objects.get(id=advertiser_id)

    deal = Deal(
            price=price, original_price=original_price, currency=currency,
            state=state, category=category, quorum=quorum,
            disclaimer=disclaimer, description=description, address=address,
            max_quantity_available=max_quantity_available, date_end=date_end,
            active=active, title=title, advertiser=advertiser,
            duration=20
    )

    deal.save()

    return deal


class DealAPITest(APITestCase):
    def setUp(self):
        user = create_test_user()
        merchant = create_merchant(user)
        deal = create_deal(merchant)
        self.client.login(username='amos', password='12345')

    def test_merchant_can_access_all_his_deals(self):
        deals = self.client.get('/api/deals/')

        first_deal = deals.data['results'][0]['title']

        self.assertIn('Sofa', first_deal)
