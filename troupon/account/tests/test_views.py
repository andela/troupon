from django.test import TestCase, Client, LiveServerTestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from selenium import webdriver

from mock import patch


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


class ForgotPasswordViewTestCase(TestCase):
    
    def setUp(self):
        # create a test client:
        self.client = Client()
        # register a sample user:
        self.user = User.objects.create_user('AwiliUzo', 'awillionaire@gmail.com', 'Young1491')
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
        response = self.client.post('/account/recovery/', {"email": self.user.email})
        
        self.assertIn('registered_user', response.context)
        self.assertIn('recovery_mail_status', response.context)
        self.assertEqual(response.context['recovery_mail_status'], 200)

    def test_recovery_email_not_sent_for_unregistered_user(self):
        response = self.client.post('/account/recovery/', {"email":"unregistereduser@andela.com" })
        self.assertNotIn('registered_user', response.context)    
        self.assertNotIn('recovery_mail_status', response.context)
# -*- coding: utf-8 -*-


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
            'admin','admin@example.com','admin')
        self.driver = webdriver.Firefox()
        super(UserRegisterTestCase, self).setUp()

    def test_signin_user(self,):
        """
        Checks if a user can sign in
        """
        self.driver.get(
            "%s%s" %(self.live_server_url, '/signin/'))

        # input login details and submit
        username = self.driver.find_element_by_id("username").send_keys('admin')
        password = self.driver.find_element_by_id("password").send_keys('admin')
        self.driver.find_element_by_xpath("//input[@value='Sign in']").click()
        
        # assert that user is logged in by accessing admin area
        self.driver.get('%s%s' % (self.live_server_url, "/admin/auth/user/add/"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self,):
        """
        Checks if user can signup on signin page
        """
        self.driver.get(
            "%s%s" %(self.live_server_url, '/signin/'))

        self.driver.find_element_by_id("user_signup_link").click()
        self.driver.find_element_by_id("create_username").send_keys("tosin")
        self.driver.find_element_by_id("create_password1").send_keys("tosin")
        self.driver.find_element_by_id("create_password2").send_keys("tosin")
        self.driver.find_element_by_id("create_email").send_keys("tosin@andela.com")
        self.driver.find_element_by_id("create_user_form").submit()
        self.assertIn("Success! your account has been created", self.driver.page_source)

    def tearDown(self,):
        """
        Close the browser window
        """
        self.driver.close()
        super(UserRegisterTestCase, self).tearDown()