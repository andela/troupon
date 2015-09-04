from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

class UserSignupTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()
