from deals.models import Deal
from account.models import Merchant
from django.conf import settings
from django.test import TestCase
from django.shortcuts import reverse
from deals.tests.test_routes import set_advertiser_and_category


class MerchantDealsTestCase(TestCase):
    """Tests that routes to manage deals are accessible by the logged in
    merchant.
    route: '/merchant/deals'
    """

    @classmethod
    def setUpClass(cls):
        deal = set_advertiser_and_category()  # dictionary
        cls.deal = Deal(**deal)
        cls.deal.save()
        cls.user = settings.AUTH_USER_MODEL.objects.create_user(
            'johndoe', 'johndoe@gmail.com', '12345'
        )

        is_merchant = Merchant.objects.filter(
            userprofile=cls.user.userprofile
        )

        if not is_merchant:
            Merchant(userprofile=cls.user.userprofile).save()

        super(MerchantDealsTestCase, cls).setUpClass()

        # login user
        response = cls.client.post(
            reverse('login'),
            dict(username='johndoe@gmail.com', password='12345')
        )
        cls.assertEquals(response.status_code, 302)

    def test_can_view_purchases_with_quantity(self):
        # Ensures that the merchant can view deals purchased
        response = self.client.get(
            reverse('merchant_deals')
        )
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        super(MerchantDealsTestCase, cls).tearDownClass()


class MerchantDealTestCase(TestCase):
    """Manage single deal under merchant role.
    route: '/merchant/deals/<slug>'
    """
    @classmethod
    def setUpClass(cls):
        deal = set_advertiser_and_category()  # dictionary
        cls.deal = Deal(**deal)
        cls.deal.save()
        cls.user = settings.AUTH_USER_MODEL.objects.create_user(
            'johndoe', 'johndoe@gmail.com', '12345'
        )

        is_merchant = Merchant.objects.filter(
            userprofile=cls.user.userprofile
        )

        if not is_merchant:
            Merchant(userprofile=cls.user.userprofile).save()

        super(MerchantDealsTestCase, cls).setUpClass()

        # login user
        response = cls.client.post(
            reverse('login'),
            dict(username='johndoe@gmail.com', password='12345')
        )
        cls.assertEquals(response.status_code, 302)

    def test_can_mark_deal_as_active(self):
        # Ensures that a merchant can mark a deal as active
        response = self.client.post(
            reverse(
                'merchant_deal', kwargs={'slug': self.deal.slug}
            ),
            data={'active': True}
        )
        self.assertTrue(self.deal.active)
        self.assertEqual(response.status_code, 302)

    def test_can_set_quantity_of_product_available(self):
        # Ensures that quantity of product available can be set to a number
        response = self.client.post(
            reverse(
                'merchant_deal', kwargs={'slug': self.deal.slug}
            ),
            data={'quantity': 360}  # stock quantity
        )
        self.assertEqual(self.deal.quantity, 360)
        self.assertEqual(response.status_code, 302)

    def test_can_view_deal_management_dashboard_for_single_deal(self):
        # 1 test_can_view_buyers_for_deal
        # 2 test_can_view_buyers
        # 3 test_can_view_sales_trends
        # 4 test_can_view_sales_trends_for_individual_deal
        # 5 test_can_view_sales_trends_for_individual_deal
        response = self.client.get(
            reverse('merchant_deal', kwargs={'slug': self.deal.slug})
        )
        # TODO: add tests for 1-5
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        super(MerchantDealsTestCase, cls).tearDownClass()
