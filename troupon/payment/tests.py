from django.test import TestCase
from selenium import webdriver
from django.test import LiveServerTestCase
from django.contrib.auth.models import User


class TestCheckoutPage(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(TestCheckoutPage, self).setUpClass()
        # create a user
        self.user = User.objects.create_user('admin',
                                             'admin@test.com',
                                             'PassPhrase22!')
        self.user.save()

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        super(TestCheckoutPage, self).setUp()

        # login the user
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        self.driver.find_element_by_id('email').send_keys("admin@test.com")
        self.driver.find_element_by_id('password').send_keys("PassPhrase22!")
        self.driver.find_element_by_id("loginBtn").click()

    def tearDown(self):
        self.driver.quit()
        super(TestCheckoutPage, self).tearDown()

    @classmethod
    def tearDownClass(self):
        super(TestCheckoutPage, self).tearDownClass()

    def test_01_checkout_page_has_stripe_button(self):
        self.driver.get('%s%s' % (self.live_server_url, '/cart/checkout/'))
        button_script = '''https://checkout.stripe.com/checkout.js'''
        self.assertIn(button_script, self.driver.page_source)
        self.assertIn('Total amount due', self.driver.page_source)
