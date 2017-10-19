from deals.models import Deal
from deals.tests.test_routes import set_advertiser_and_category
from merchant.models import Merchant
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, LiveServerTestCase
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC


class MerchantManageDealsTestCase(TestCase):
    """Tests that routes to manage deals are accessible by the logged in
    merchant.
    route: '/merchant/deals'
    """

    @classmethod
    def setUpClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()
        deal = set_advertiser_and_category()  # dictionary
        cls.deal = Deal(**deal)
        cls.deal.save()
        cls.user = User.objects.create_user(
            'testuser1', 'testuser1@mail.com', '12345'
        )

        is_merchant = cls.user.profile.is_approved_merchant()

        if not is_merchant:
            cls.merchant = Merchant(
                advertiser_ptr=cls.deal.advertiser,
                userprofile=cls.user.profile,
                enabled=True,
                approved=True,
                intlnumber='123456789'
            )
            cls.merchant.save()

        cls.client = Client()
        super(MerchantManageDealsTestCase, cls).setUpClass()

    def test_can_login_user(self):
        # login user
        response = self.client.post(
            reverse('login'),
            dict(username='testuser1@mail.com', password='12345')
        )
        self.assertEquals(response.status_code, 302)

    def test_can_view_purchases_with_quantity(self):
        # Ensures that the merchant can view deals purchased
        response = self.client.post(
            reverse('login'),
            dict(username='testuser1@mail.com', password='12345')
        )
        response = self.client.get(
            reverse('merchant_manage_deals')
        )
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()
        super(MerchantManageDealsTestCase, cls).tearDownClass()


class MerchantManageDealTestCase(TestCase):
    """Manage single deal under merchant role.
    route: '/merchant/deals/<slug>'
    """
    @classmethod
    def setUpClass(cls):
        Deal.objects.all().delete()
        deal = set_advertiser_and_category()  # dictionary
        cls.deal = Deal(**deal)
        cls.deal.save()
        cls.user = User.objects.create_user(
            username='testuser2', email='testuser2@mail.com', password='12345',
        )

        is_merchant = cls.user.profile.is_approved_merchant()

        if not is_merchant:
            cls.merchant = Merchant(
                advertiser_ptr=cls.deal.advertiser,
                userprofile=cls.user.profile,
                enabled=True,
                approved=True,
                intlnumber='123456789'
            )
            cls.merchant.save()

        cls.client = Client()
        super(MerchantManageDealTestCase, cls).setUpClass()

    def test_can_login_user(self):
        # login user
        response = self.client.post(
            reverse('login'),
            dict(username='testuser2@mail.com', password='12345')
        )
        self.assertEquals(response.status_code, 302)

    def test_can_mark_deal_as_active(self):
        # Ensures that a merchant can mark a deal as active
        response = self.client.post(
            reverse('login'),
            dict(username='testuser2@mail.com', password='12345')
        )
        response = self.client.post(
            reverse(
                'merchant_manage_deal', kwargs={'deal_slug': self.deal.slug}
            ),
            data={'active': True}
        )
        self.assertTrue(self.deal.active)
        self.assertEqual(response.status_code, 302)

    def test_can_set_quantity_of_product_available(self):
        # Ensures that quantity of product available can be set to a number
        response = self.client.post(
            reverse('login'),
            dict(username='testuser2@mail.com', password='12345')
        )
        response = self.client.post(
            reverse(
                'merchant_manage_deal', kwargs={'deal_slug': self.deal.slug}
            ),
            data={'max_quantity_available': 360}  # stock quantity
        )

        self.deal = Deal.objects.get(
            slug=self.deal.slug
        )  # refresh cached object
        self.assertEqual(self.deal.max_quantity_available, 360)
        self.assertEqual(response.status_code, 302)

    @classmethod
    def tearDownClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()
        super(MerchantManageDealTestCase, cls).tearDownClass()


class SalesHistoryAndTrendTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        deal = set_advertiser_and_category()
        deal['title'] = 'Deal #3'  # dictionary
        cls.deal = Deal(**deal)
        cls.deal.save()
        cls.user = User.objects.create_user(
            'testuser3', 'testuser3@mail.com', '123456'
        )

        is_merchant = cls.user.profile.is_approved_merchant()

        if not is_merchant:
            cls.merchant = Merchant(
                advertiser_ptr=cls.deal.advertiser,
                userprofile=cls.user.profile,
                enabled=True,
                approved=True,
                intlnumber='123456789'
            )
            cls.merchant.save()
        cls.selenium = webdriver.Chrome()
        cls.wait = ui.WebDriverWait(cls.selenium, 10)
        super(SalesHistoryAndTrendTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()
        cls.selenium.quit()
        super(SalesHistoryAndTrendTestCase, cls).tearDownClass()

    def test_can_view_deal_management_dashboard_for_single_deal(self):
        """Test that a merchant can access deal management options on his
        dashboard
        """
        self.selenium.get('%s%s' % (self.live_server_url, reverse('login')))
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//input[@value="Log in"]')
            )
        )
        username_input = self.selenium.find_element_by_id("email")
        username_input.send_keys('testuser3@mail.com')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_xpath(
            '//input[@value="Log in"]').click()

        self.selenium.get(
            '%s%s' % (self.live_server_url, reverse(
                'merchant_manage_deal', kwargs={'deal_slug': self.deal.slug})
            )
        )
        # 1 test_can_view_buyers_of_this_deal
        self.selenium.find_element_by_xpath(
            '//li[.="Sales History"]').click()
        self.selenium.find_element_by_xpath(
            '//h4[.="All purchases of your merchandise"]')
        el = self.selenium.find_element_by_xpath('//th[.="Buyer"]')
        self.assertIsNotNone(el)

        # 2 test_can_view_sales_trends_for_deal
        self.selenium.find_element_by_xpath(
            '//li[.="Sales Trend"]').click()
        self.selenium.find_element_by_xpath(
            '//h4[.="Monthly sales trend"]')
        el = self.selenium.find_element_by_id('visualisation')
        self.assertIsNotNone(el)
