import mock

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.importlib import import_module
from django.conf import settings

from userprofile.models import Merchant
from userprofile.views import MerchantView, VerificationView


class UserProfileTestCase(TestCase):

    def setUp(self):
        '''
        User calls profile page.
        '''
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='johndoe',
                                             email='johndoe@gmail.com',
                                             password='12345')
        self.client.login(username='johndoe', password='12345')


class TestProfileAction(UserProfileTestCase):

    def test_user_calls_profilepage(self):

        response = self.client.get("/userprofile/johndoe")
        self.assertEquals(response.status_code, 200)

    def test_user_update_profile(self):

        data = dict(first_name='joe', last_name='doe', interest='Games')
        response = self.client.get("/userprofile/johndoe", data)
        self.assertEquals(response.status_code, 200)

    def test_update_errors(self):

        data = dict(first_name='', last_name='', interest='')
        response = self.client.get("/userprofile/johndoe", data)
        self.assertEquals(response.status_code, 200)


class TestMerchantView(UserProfileTestCase):

    def test_user_view_merchant_form(self):

        response = self.client.get(reverse('merchant'))
        self.assertEquals(response.status_code, 200)

    def test_user_register_as_merchant(self):

        data = {
            'name': 'yourname',
            'user_state': 25,
            'telephone': '123456789020',
            'email': 'youremail',
            'address': 'youraddress',
            'slug': 'yourslug'
        }
        with mock.patch(
            'nexmo.libpynexmo.nexmomessage.NexmoMessage.send_request')\
                as mock_send_request:

            mock_send_request.return_value = (
                {"return": {"return": "return"}})
            merchant = Merchant()
            merchant.save = mock.MagicMock(name='save')
            request = self.factory.post(reverse('merchant'), data)
            request.user = self.user
            engine = import_module(settings.SESSION_ENGINE)
            session_key = None
            request.session = engine.SessionStore(session_key)
            response = MerchantView.as_view()(request)
            self.assertEquals(response.status_code, 200)


class TestOTPVerification(UserProfileTestCase):

    def test_otp_form_shown(self):

        response = self.client.get(reverse('verify'))
        self.assertEquals(response.status_code, 200)

    def test_otp_number_verified(self):

        data = {'token': 12345}

        with mock.patch('pyotp.TOTP.verify') as mock_verify:
            mock_verify.return_value = True
            request = self.factory.post(reverse('verify'), data)
            response = VerificationView.as_view()(request)
            self.assertEquals(response.status_code, 200)
