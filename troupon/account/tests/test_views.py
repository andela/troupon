from django.test import TestCase, Client, LiveServerTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mock import patch
import socket

class UserSignInViewTestCase(TestCase):
    """Test that post and get requests to signin routes is successful
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_view_get_auth_signin(self):
        """Test that user request for signin page binds to a view called
            the class name `UserSigninView`.
        """

        response = resolve('/account/signin/')
        self.assertEquals(response.func.__name__, 'UserSigninView')

    def test_view_post_auth_signin(self):
        """Test that user post to signin route has a session
        """
        data = {'username': 'johndoe@gmail.com', 'password': '12345'}
        response = self.client.post('/account/signin/', data)
        self.assertIn('deals', response.content)


class UserSignoutRouteTestCase(TestCase):
    """Test that user can signout of session.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('johndoe',
                                             'johndoe@gmail.com',
                                             '12345')

    def test_route_get_auth_signout(self):
        self.client.post('/account/signin',
                         dict(username='johndoe@gmail.com',
                              password='12345'))
        response = self.client.get('/account/signout/')
        self.assertIsNone(response.context)
        self.assertEquals(response.status_code, 302)


class ForgotPasswordViewTestCase(TestCase):

    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.user = User.objects.create_user(
            'AwiliUzo', 'awillionaire@gmail.com', 'Young1491')
        self.user.first_name = 'Uzo'
        self.user.last_name = 'Awili'
        self.user.save()

    def test_get_returns_200(self):
        response = self.client.get('/account/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_post_returns_200(self):
        response = self.client.get('/account/recovery/')
        self.assertEquals(response.status_code, 200)

    def test_recovery_email_sent_for_registered_user(self):
        response = self.client.post(
            '/account/recovery/', {"email": self.user.email})

        self.assertIn('registered_user', response.context)
        self.assertIn('recovery_mail_status', response.context)
        self.assertEqual(response.context['recovery_mail_status'], 200)

    def test_recovery_email_not_sent_for_unregistered_user(self):
        response = self.client.post(
            '/account/recovery/', {"email": "unregistereduser@andela.com"})
        self.assertNotIn('registered_user', response.context)
        self.assertNotIn('recovery_mail_status', response.context)


# selenium tests for registration, signup and signin templates
class UserRegisterTestCase(LiveServerTestCase):
    '''
    End to End testing of user registration and signin pages
    '''

    def setUp(self,):
        """
        Setup the test driver
        """
        User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin')
        self.driver = webdriver.PhantomJS()
        super(UserRegisterTestCase, self).setUp()

        # socket.setdefaulttimeout(10)

    def test_signin_user(self,):
        """
        Checks if a user can sign in
        """
        url = "%s%s" % (self.live_server_url, reverse('signin'))
        self.driver.get(url)
        # input login details and submit
        self.driver.find_element_by_id("username").send_keys('admin')
        self.driver.find_element_by_id("password").send_keys('admin')
        self.driver.find_element_by_xpath("//input[@value='Sign in']").click()
        # assert that user is logged in by accessing admin area
        self.driver.get(
            '%s%s' % (self.live_server_url, "/admin/auth/user/add/"))
        self.assertIn('Add user', self.driver.page_source)

    # def test_user_can_register(self,):
    #     """
    #     Checks if user can signup on signin page
    #     """
    #     url = "%s%s" % (self.live_server_url, reverse('signin'))
    #     self.driver.get(url)
    #     self.driver.find_element_by_id("user_signup_link").click()
    #     block = WebDriverWait(self.driver, 10)
    #     # by = self.driver.find_element_by_class_name('bs-example-modal-lg')
    #     block.until(
    #         EC.visibility_of_element_located(
    #             (By.CLASS_NAME, 'bs-example-modal-lg')
    #             )
    #         )
    #     self.driver.find_element_by_id("createUsername").send_keys("tosin")
    #     self.driver.find_element_by_id("createPassword1").send_keys("tosin")
    #     self.driver.find_element_by_id("createPassword2").send_keys("tosin")
    #     self.driver.find_element_by_id(
    #         "createEmail"
    #         ).send_keys("tosin@andela.com")
    #     self.driver.find_element_by_name("createUserForm").submit()
    #     # self.assertIn("Success! your account has been created", self.driver.page_source)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.quit()
        super(UserRegisterTestCase, self).tearDown()
