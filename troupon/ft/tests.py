from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

class UserSignupTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_User_Signup(self):
    # user opens web browser, navigates to home page
    self.browser.get(self.live_server_url + '/')
    # user clicks on the signup link
    signup_link = self.browser.find_elements_by_link_text('Sign Up')
    signup_link[0].click()
    # user fills out the form
    self.browser.find_element_by_name('first_name').send_keys("andela")
    self.browser.find_element_by_name('last_name').send_keys("andela")
    self.browser.find_element_by_name('email').send_keys("samuel.james@andelacom")
    # user clicks the Register button
    self.browser.find_element_by_css_selector("input[value='Register']").click()
    # the user has been registered
    body = self.browser.find_element_by_tag_name('body')
    self.assertIn('samuel.james@andela.com', body.text)

