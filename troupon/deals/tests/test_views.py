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
        Checks if the homepage title is correct
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Troupon - Get Some!", driver.title)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
