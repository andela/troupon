"""Import Statements."""
import unittest
from merchant.models import Merchant
from account.models import UserProfile
from django.contrib.auth.models import User
from deals.models import Deal, Category, Advertiser
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
TEST_USER_EMAIL = 'testuser@email.com'
TEST_USER_PASSWORD = 'testpassword'


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
            userprofile=self.create_user_profile(), intlnumber='238974', enabled=True, approved=True, trusted=True)
        return merchant

    def create_user_profile(self):
        """Creates the test userprofile"""
        user_object = User.objects.all()[:1].get()
        user_profile = UserProfile.objects.create(
            user=user_object, user_state=25, occupation='Business man', intlnumber='238974')
        return user_profile

    def create_deal(self):
        """Creates the test deal"""
        merchant = self.create_merchant()
        price = 200
        original_price = 100
        currency = 2
        state = 2
        quorum = 0
        disclaimer = 'fdg'
        description = 'This is a phone'
        title = 'Phone'
        address = '3820-00100'
        max_quantity_available = 20
        active = True
        advertiser_id = merchant.advertiser_ptr.id
        date_end = "2015-03-03"

        category = Category.objects.create(name="Electronics", slug="stuff")

        # category = Category.objects.get(id=category_id)
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


class AddToCartViewTest(LiveServerTestCase, AuthenticateAddDeal):
    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(AddToCartViewTest, self).setUp()

    def test_add_to_cart(self):
        """Gets an item and adds to cart"""

        self.create_user()
        self.create_deal()
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div/main/section[2]/div[2]/div/div[3]/form/button").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        text_quantity = self.driver.find_element_by_xpath(
            "//li/ul/li[@class='pull-right']/h6/small/strong/span[@class='badge']").text  # get items quantity

        assert "Quantity: 1" in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(AddToCartViewTest, self).tearDown()


class ViewCartViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
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
            "/html/body/div/div[1]/div/main/section[2]/div[2]/div/div[3]/form/button").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            "//a[@class='btn-action'][1]").click()  # clicks view cart
        cart_label = self.driver.find_element_by_xpath(
            "//h1[@class='title']").text  # gets cart items title
        assert "Your Cart Items" in cart_label

    def tearDown(self):
        self.driver.quit()
        super(ViewCartViewTest, self).tearDown()


class ClearCartViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
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
            "/html/body/div/div[1]/div/main/section[2]/div[2]/div/div[3]/form/button").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            "//a[@class='btn-action'][2]").click()  # clicks clear cart button
        text_quantity = self.driver.find_element_by_xpath(
            "//ul[@class='dropdown-menu dropdown-menu-right']/div[@class='dropdown-header']/p[1]").text  # get items quantity if any
        assert "Quantity: 1" not in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(ClearCartViewTest, self).tearDown()


class RemoveItemViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
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
            "//div[@class='grid-item card'][1]/form[@class='overlay row']/button[@class='btn-action cta-button']").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            "//li[1]/ul/li[@class='pull-left']/form/button[@class='btn btn-sm']").click()  # clicks remove cart button
        text_quantity = self.driver.find_element_by_xpath(
            "//ul[@class='dropdown-menu dropdown-menu-right']/div[@class='dropdown-header']/p[1]").text  # get items quantity if any
        assert "Quantity: 1" not in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(RemoveItemViewTest, self).tearDown()


class CheckoutViewTest(LiveServerTestCase, AuthenticateAddDeal):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
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
            "//div[@class='grid-item card'][1]/form[@class='overlay row']/button[@class='btn-action cta-button']").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        self.driver.find_element_by_xpath(
            "//a[@class='btn-action'][1]").click()  # clicks view cart
        cart_label = self.driver.find_element_by_xpath(
            "//h1[@class='title']").text  # gets cart items title
        #clicks the proceed to checkout button
        self.driver.find_element_by_xpath(
            "//div[@class='pull-right col-sm-2']/a[@class='btn-action']").click()
        pay_card_label = self.driver.find_element_by_xpath(
            "//div[@class='text-center']/form[@class='form-checkout']/button[@class='stripe-button-el']/span").text
        assert "Pay with Card" in pay_card_label

    def tearDown(self):
        self.driver.quit()
        super(CheckoutViewTest, self).tearDown()


if __name__ == "__main__":
    unittest.main()
