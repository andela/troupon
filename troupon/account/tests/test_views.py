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
    def setUp(self,):
        User.objects.create_superuser('admin','admin@example.com','admin')
        self.driver = webdriver.Firefox()
        super(UserRegisterTestCase, self).setUp()

    

    def tearDown(self,):
        self.driver.close()
        super(UserRegisterTestCase, self).tearDown()