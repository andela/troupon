"""Import Statements."""
import unittest

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver

from accounts.models import UserProfile
from deals.models import Advertiser, Category, Deal
from merchant.models import Merchant

TEST_USER_EMAIL = 'testuser@email.com'
TEST_USER_PASSWORD = 'testpassword'

xpath_first_deal_item = "//div[@class='row']/button[@class='btn-action cta-button']"
xpath_checkout_basket = "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']"
xpath_items_quantity_text = "//li/ul/li[@class='pull-right']/h6/small/strong/span[@class='badge']"
xpath_view_cart = "//a[@class='btn-action'][1]"
xpath_cart_items_title = "//h1[@class='title']"
xpath_clear_cart_button = "//a[@class='btn-action'][2]"
xpath_items_quantity = "//ul[@class='dropdown-menu dropdown-menu-right']/div[@class='dropdown-header']/p[1]"
xpath_remove_cart_button = "//li[1]/ul/li[@class='pull-left']/form/button[@class='btn btn-sm']"
xpath_checkout_button = "//div[@class='pull-right col-sm-2']/a[@class='btn-action']"
xpath_paycard_label = "//div[@class='text-center']/form[@class='form-checkout']/button[@class='stripe-button-el']/span"
xpath_proceed_to_pay = "//div[@class='center-buttons']/div/input[@class='btn-action btn-form-submit']"


class AuthenticateAddDeal():
    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % (self.live_server_url, "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def create_user(self):
        """Creates the test user"""
        User.objects.create_user(username='testuser',
                                 email='testuser@email.com',
                                 password='testpassword')

    def create_merchant(self):
        """Creates the test merchant"""
        merchant = Merchant.objects.create(
            userprofile=self.create_user_profile(), intlnumber='238974',
            enabled=True, approved=True, trusted=True)
        return merchant

    def create_user_profile(self):
        """Creates the test userprofile"""
        user_object = User.objects.all()[:1].get()
        user_profile = UserProfile.objects.create(
            user=user_object, country=2, location=84,
            occupation='Business man', intlnumber='238974')
        return user_profile

    def create_deal(self):
        """Create the test deal"""
        merchant = self.create_merchant()
        price = 5000
        original_price = 6000
        currency = 1
        country = 2
        location = 84
        quorum = 0
        disclaimer = ''
        description = 'Holiday for two to the luxurious Masai Mara.'
        title = 'Masai Mara Holiday'
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


class AddToCartViewTest(LiveServerTestCase, AuthenticateAddDeal):
    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(AddToCartViewTest, self).setUp()

    def test_add_to_cart(self):
        """Gets an item and adds to cart"""

        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(xpath_first_deal_item
                                          ).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        text_quantity = self.driver.find_element_by_xpath(
            xpath_items_quantity_text).text  # get items quantity

        assert "Quantity: 1" in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(AddToCartViewTest, self).tearDown()


class ViewCartViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(ViewCartViewTest, self).setUp()

    def test_view_cart(self):
        """Gets an item and adds to cart and opens view for the cart"""
        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            xpath_first_deal_item).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(xpath_view_cart
                                          ).click()  # clicks view cart
        cart_label = self.driver.find_element_by_xpath(
            xpath_cart_items_title).text  # gets cart items title
        assert "Your Cart Items" in cart_label

    def tearDown(self):
        self.driver.quit()
        super(ViewCartViewTest, self).tearDown()


class ClearCartViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(ClearCartViewTest, self).setUp()

    def test_clear_cart(self):
        """Clears the cart of all items"""
        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            xpath_first_deal_item).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            xpath_clear_cart_button).click()  # clicks clear cart button
        text_quantity = self.driver.find_element_by_xpath(
            xpath_items_quantity).text  # get items quantity
        assert "Quantity: 1" not in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(ClearCartViewTest, self).tearDown()


class AddShippingDetailsTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(AddShippingDetailsTest, self).setUp()

    def test_view_cart(self):
        """Adds user details to the shipping details form and redirects to pay page"""
        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            xpath_first_deal_item).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            xpath_view_cart).click()  # clicks view cart
        # clicks the proceed to checkout button
        self.driver.find_element_by_xpath(
            xpath_checkout_button).click()
        self.driver.find_element_by_id("street").send_keys('12345')
        self.driver.find_element_by_id("postal").send_keys('5678')
        self.driver.find_element_by_id("state").send_keys('states')
        self.driver.find_element_by_id("telephone").send_keys('0794284244')
        # clicks the proceed to pay button
        self.driver.find_element_by_xpath(
            xpath_proceed_to_pay).click()

    def tearDown(self):
        self.driver.quit()
        super(AddShippingDetailsTest, self).tearDown()


class RemoveItemViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(RemoveItemViewTest, self).setUp()

    def test_remove_items(self):
        """Gets an item and removes it from cart"""
        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            xpath_first_deal_item).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            xpath_remove_cart_button).click()  # clicks remove cart button
        text_quantity = self.driver.find_element_by_xpath(
            xpath_items_quantity).text  # get items quantity after removing item
        assert "Quantity: 1" not in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(RemoveItemViewTest, self).tearDown()


class CheckoutViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        super(CheckoutViewTest, self).setUp()

    def test_checkout_view(self):
        """Opens view for checking out items"""
        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            xpath_first_deal_item).click()  # click first item
        self.driver.find_element_by_xpath(
            xpath_checkout_basket).click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            xpath_view_cart).click()  # clicks view cart
        # clicks the proceed to checkout button
        self.driver.find_element_by_xpath(
            xpath_checkout_button).click()

    def tearDown(self):
        self.driver.quit()
        super(CheckoutViewTest, self).tearDown()


if __name__ == "__main__":
    unittest.main()
