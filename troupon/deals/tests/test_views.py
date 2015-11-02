import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class HomepageViewTests(LiveServerTestCase):
    """runs functional tests for the homepage"""

    @classmethod
    def setUpClass(cls):
        """
        Setup the test driver
        """
        cls.driver = webdriver.PhantomJS()
        super(HomepageViewTests, cls).setUpClass()

    def setUp(self,):
        """
        Setup the test driver
        """
        self.driver = HomepageViewTests.driver
        super(HomepageViewTests, self).setUp()

    def test_title(self,):
        """
        Checks homepage displays correct title
        """
        self.driver.get(self.live_server_url + '/')
        self.assertIn("Troupon - Get Some", self.driver.title)

    def test_can_subscribe(self,):
        """
        Checks if newsletter form is present on homepage
        """
        self.driver.get("%s" % (self.live_server_url))
        self.assertTrue("driver.find_element_by_id('subscriberEmail')")

    def test_about_us_present(self,):
        """
        Checks if the about us section is present in homepage
        """
        self.driver.get(self.live_server_url + '/')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn("About", body.text)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.quit() 
        super(HomepageViewTests, self).tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(HomepageViewTests, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
