import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class HomepageViewTests(LiveServerTestCase):
    """runs functional tests for the homepage"""

    def setUp(self,):
        """
        Setup the test driver
        """
        self.driver = webdriver.Firefox()
        super(HomepageViewTests, self).setUp()

    def test_title(self,):
        """
        Checks homepage displays correct title
        """
        driver = self.driver
        driver.get("%s" %(self.live_server_url))
        self.assertIn("Troupon - Get Some!", driver.title)

    def test_can_subscribe(self,):
        """
        Checks if newsletter form is present on homepage
        """
        driver = self.driver
        driver.get("%s" %(self.live_server_url))
        self.assertTrue("driver.find_element_by_name('subscriber_email')")

    def test_about_us_present(self,):
        """
        Checks if the about us section is present in homepage
        """
        driver = self.driver
        driver.get("%s" %(self.live_server_url))
        assert "About Troupon" in driver.page_source

    def test_social_links(self,):
        """
        Checks social links are working
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        assert "http://facebook.com/troupon/" in driver.page_source
        assert "http://twitter.com/troupon/" in driver.page_source

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()
        super(HomepageViewTests, self).tearDown()

if __name__ == "__main__":
    unittest.main()