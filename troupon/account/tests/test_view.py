import mock

from django.core.urlresolvers import reverse
from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage


from account.tests.test_routes import UserProfileTestCase
from account.views import MerchantRegisterView, MerchantVerifyVeiw, \
    MerchantResendOtpVeiw, MerchantConfirmVeiw


class TestMerchantView(UserProfileTestCase):

    def test_user_can_view_merchant_page(self):

        response = self.client.get(reverse('account_merchant'))
        self.assertEquals(response.status_code, 200)

    def test_user_register_as_merchant(self):

        data = {
            'name': 'yourname',
            'user_state': 25,
            'telephone': '12345678901',
            'intlnumber': '+2342345678901',
            'email': 'youremail',
            'address': 'youraddress',
            'slug': 'yourslug',
        }
        data2 = {'token': 123456}

        with mock.patch(
            'nexmo.libpynexmo.nexmomessage.NexmoMessage.send_request')\
                as mock_send_request:

                mock_send_request.return_value = (
                    {"return": {"return": "return"}}
                )

                request = self.factory.post(
                    reverse('account_merchant_register'),
                    data)
                request.user = self.user
                engine = import_module(settings.SESSION_ENGINE)
                session_key = None
                request.session = engine.SessionStore(session_key)
                response = MerchantRegisterView.as_view()(request)
                self.assertEquals(response.status_code, 302)

        # test that OTP number is verified
        with mock.patch('pyotp.TOTP.verify') as mock_verify:
            mock_verify.return_value = True
            request = self.factory.post(
                reverse('account_merchant_verify'), data2)
            request.user = self.user
            engine = import_module(settings.SESSION_ENGINE)
            session_key = None
            request.session = engine.SessionStore(session_key)
            response = MerchantVerifyVeiw.as_view()(request)
            self.assertEquals(response.status_code, 302)

        # test OTP resend view
        with mock.patch(
            'nexmo.libpynexmo.nexmomessage.NexmoMessage.send_request')\
                as mock_send_request:

                mock_send_request.return_value = (
                    {"return": {"return": "return"}}
                )

                request = self.factory.get(
                    reverse('account_merchant_resendotp'),
                    data)
                request.user = self.user
                engine = import_module(settings.SESSION_ENGINE)
                session_key = None
                request.session = engine.SessionStore(session_key)
                messages = FallbackStorage(request)
                setattr(request, '_messages', messages)
                response = MerchantResendOtpVeiw.as_view()(request)
                self.assertEquals(response.status_code, 302)


class TestOTPVerification(UserProfileTestCase):

    def test_otp_form_shown(self):

        response = self.client.get(reverse('account_merchant_verify'))
        self.assertEquals(response.status_code, 200)


class TestMerchantConfirmationView(UserProfileTestCase):

    def test_confirmation_page_can_be_viewed(self):

        request = self.factory.get(
            reverse('account_merchant_confirm'))
        request.user = self.user
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = MerchantConfirmVeiw.as_view()(request)
        self.assertEquals(response.status_code, 200)
