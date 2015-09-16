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
        self.driver = webdriver.PhantomJS()
        super(HomepageViewTests, self).setUp()

    def test_title(self,):
        """
        Checks homepage displays correct title
        """
        self.driver.get(self.live_server_url + '/')
        head = self.driver.find_element_by_tag_name('head')
        self.assertIn("Troupon - Get Some!", head.text)


    def test_can_subscribe(self,):
        """
        Checks if newsletter form is present on homepage
        """
        self.driver.get("%s" %(self.live_server_url))
        self.assertTrue("driver.find_element_by_name('subscriber_email')")

    def test_about_us_present(self,):
        """
        Checks if the about us section is present in homepage
        """
        self.driver.get(self.live_server_url + '/')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn("About Troupon", body.text)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()
        super(HomepageViewTests, self).tearDown()

if __name__ == "__main__":
    unittest.main()