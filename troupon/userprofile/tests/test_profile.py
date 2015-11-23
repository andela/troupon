from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from allaccess.views import OAuthRedirect,OAuthCallback


class UserProfileTestCase(TestCase):

    def setUp(self):
        '''
        User calls profile page.
        '''
        self.client_stub = Client()

        self.user = User.objects.create_user(username='johndoe',
        email='johndoe@gmail.com', password='12345')

    def test_user_calls_profilepage(self):

        response = self.client_stub.get("/userprofile/user/johndoe")
        self.assertEquals(response.status_code, 302)

    def test_user_update_profile(self):

        data = dict(first_name='joe', last_name='doe', interest='Games')
        response = self.client_stub.get("/userprofile/user/johndoe", data)
        self.assertEquals(response.status_code, 302)

    def test_update_errors(self):

        data = dict(first_name='', last_name='', interest='')
        response = self.client_stub.get("/userprofile/user/johndoe", data)
        self.assertEquals(response.status_code, 302)