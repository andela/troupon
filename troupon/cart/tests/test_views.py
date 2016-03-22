"""Import Statements."""
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver

TEST_USER_EMAIL = 'jack.wachira@andela.com'
TEST_USER_PASSWORD = 'administrator'


class AddToCartViewTest(LiveServerTestCase):
    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(AddToCartViewTest, self).setUp()

    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % ("localhost:8000", "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_add_to_cart(self):
        """Gets an item and adds to cart"""

        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            "//div[@class='grid-item card'][1]/form[@class='overlay row']/button[@class='btn-action cta-button']").click()  # click first item
        self.driver.find_element_by_xpath(
            "//li[@class='dropdown'][1]/a[@class='dropdown-toggle']").click()  # click checkout basket
        self.driver.implicitly_wait(20)
        text_quantity = self.driver.find_element_by_xpath(
            "//li/ul/li[@class='pull-right']/h6/small/strong/span[@class='badge']").text  # get items quantity

        assert "Quantity: 1" in text_quantity

    def tearDown(self):
        self.driver.quit()
        super(AddToCartViewTest, self).tearDown()


class ViewCartViewTest(LiveServerTestCase):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(ViewCartViewTest, self).setUp()

    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % ("localhost:8000", "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_view_cart(self):
        """Gets an item and adds to cart and opens view for the cart"""
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
        assert "Your Cart Items" in cart_label

    def tearDown(self):
        self.driver.quit()
        super(ViewCartViewTest, self).tearDown()


class ClearCartViewTest(LiveServerTestCase):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(ClearCartViewTest, self).setUp()

    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % ("localhost:8000", "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_clear_cart(self):
        """Clears the cart of all items"""
        self.login_user()
        self.driver.execute_script("window.scrollTo(0, 400)")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(
            "//div[@class='grid-item card'][1]/form[@class='overlay row']/button[@class='btn-action cta-button']").click()  # click first item
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


class RemoveItemViewTest(LiveServerTestCase):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(RemoveItemViewTest, self).setUp()

    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % ("localhost:8000", "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_remove_items(self):
        """Gets an item and removes it from cart"""
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


class CheckoutViewTest(LiveServerTestCase):

    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(CheckoutViewTest, self).setUp()

    def login_user(self):
        """Logs in the test user"""
        self.driver.get(
            '%s%s' % ("localhost:8000", "/login/")
        )
        self.driver.find_element_by_id('email').send_keys(TEST_USER_EMAIL)
        self.driver.find_element_by_id(
            'password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_checkout_view(self):
        """Opens view for checking out items"""
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
        # clicks the proceed to checkout button
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
