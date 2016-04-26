"""Import Statements."""
import unittest
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

TEST_USER_EMAIL = 'amos.omondi@andela.com'
TEST_USER_PASSWORD = '12345'


class AddToCartViewTest(StaticLiveServerTestCase):
    def setUp(self):
        """Setup the test driver."""
        self.driver = webdriver.Firefox()

    def login_user(self):
        """Logs in the test user before the test."""
        self.driver.get(self.live_server_url + '/login/')
        username_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('password')
        username_field.send_keys(TEST_USER_EMAIL)
        password_field.send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_id("loginBtn").click()

    def test_unauthorized_user_login_redirect(self):
        """Checks unauthorized user redirect to login when accessing cart page."""
        self.driver.get(self.live_server_url + '/cart/view/')
        link = self.driver.find_element_by_id('user_register_link')
        self.assertIn("Register Here", link.text)


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
