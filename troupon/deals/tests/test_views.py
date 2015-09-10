import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HomepageViewTests(unittest.TestCase):
    """runs functional tests for the homepage"""

    def setUp(self,):
        """
        Setup the test driver
        """
        self.driver = webdriver.Firefox()

    def test_title(self,):
        """
        Checks homepage displays correct title
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Troupon - Get Some!", driver.title)

    def test_can_subscribe(self,):
        """
        Checks if newsletter form is present on homepage
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertTrue("driver.find_element_by_name('subscriber_email')")

    def test_about_us_present(self,):
        """
        Checks if the about us section is present in homepage
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        assert "About Troupon" in driver.page_source

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
