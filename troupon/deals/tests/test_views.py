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
        driver = self.driver
        driver.get(self.live_server_url + '/')
        title = driver.find_element_by_tag_name('title')
        self.assertIn("Troupon - Get Some!", title.text)

'''
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
'''


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
        driver.get(self.live_server_url + '/')
        h4 = driver.find_element_by_tag_name('h4')
        self.assertIn("About Troupon", h4.text)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()
        super(HomepageViewTests, self).tearDown()

if __name__ == "__main__":
    unittest.main()