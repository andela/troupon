import mock

from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import QueryDict
from django.core.urlresolvers import reverse
from django.utils.importlib import import_module

from accounts.tests.test_routes import UserProfileTestCase,\
    UserProfileMerchantTestCase
from accounts.views import MerchantRegisterView, MerchantVerifyView, \
    MerchantResendOtpView, MerchantConfirmView


class TestMerchantView(UserProfileMerchantTestCase):

    def test_unapproved_merchant_redirected(self):

        response = self.client.get(reverse('account_merchant'))
        self.assertEquals(response.status_code, 302)

    def test_user_register_as_merchant(self):

        data = {
            'name': 'yourname',
            'country': 2,
            'location': 84,
            'telephone': '12345678901',
            'intlnumber': '+2342345678901',
            'email': 'youremail',
            'address': 'youraddress',
            'slug': 'yourslug',
        }
        data2 = {'token': 123456}

        # test response without adding logo field to request
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
                messages = FallbackStorage(request)
                setattr(request, '_messages', messages)
                response = MerchantRegisterView.as_view()(request)
                self.assertEquals(response.status_code, 200)

        # test with addtion of logo field to request
        data['logo'] = 'iu_0jdfj.png'
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
                messages = FallbackStorage(request)
                setattr(request, '_messages', messages)
                response = MerchantRegisterView.as_view()(request)
                self.assertEquals(response.status_code, 200)

        # test failed OTP send
        with mock.patch(
            'nexmo.libpynexmo.nexmomessage.NexmoMessage.send_request')\
                as mock_send_request:

                mock_send_request.return_value = (
                    False
                )

                request = self.factory.post(
                    reverse('account_merchant_register'),
                    data
                )
                request.user = self.user
                engine = import_module(settings.SESSION_ENGINE)
                session_key = None
                request.session = engine.SessionStore(session_key)
                messages = FallbackStorage(request)
                setattr(request, '_messages', messages)
                response = MerchantRegisterView.as_view()(request)
                self.assertEquals(response.status_code, 200)

        # test that OTP number is verified
        with mock.patch('pyotp.TOTP.verify') as mock_verify:
            mock_verify.return_value = True
            request = self.factory.post(
                reverse('account_merchant_verify'), data2)
            request.user = self.user
            engine = import_module(settings.SESSION_ENGINE)
            session_key = None
            request.session = engine.SessionStore(session_key)
            response = MerchantVerifyView.as_view()(request)
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
                response = MerchantResendOtpView.as_view()(request)
                self.assertEquals(response.status_code, 302)


class TestOTPVerification(UserProfileTestCase):

    def test_otp_form_not_shown__to_user(self):

        response = self.client.get(reverse('account_merchant_verify'))
        self.assertEquals(response.status_code, 302)

    def test_confirmation_page_cannot_be_viewed_by_user(self):

        request = self.factory.get(
            reverse('account_merchant_confirm'))
        request.user = self.user
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = MerchantConfirmView.as_view()(request)
        self.assertEquals(response.status_code, 302)


class TestMerchantConfirmationView(UserProfileMerchantTestCase):

    def test_confirmation_page_can_be_viewed_by_merchant(self):

        request = self.factory.get(
            reverse('account_merchant_confirm'))
        request.user = self.user
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = MerchantConfirmView.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TransactionsViewTestCase(UserProfileTestCase):
    """Suite of tests for transaction view"""

    def test_transaction_history_cannot_be_viewed_by_unauthenticated_users(
            self):
        self.client.logout()
        response = self.client.get(reverse('account_history'))
        self.assertEquals(response.status_code, 302)

    def test_transaction_history_without_page_number(self):
        response = self.client.get(reverse('account_history'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['transactions'].number, 1)

    def test_transaction_history_with_page_number_in_url(self):
        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update({'pg': 1})
        url = '{base_url}?{querystring}'.format(
            base_url=reverse('account_history'),
            querystring=query_dictionary.urlencode()
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['transactions'].number, 1)

    def test_transaction_history_with_empty_page(self):
        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update({'pg': 2})
        url = '{base_url}?{querystring}'.format(
            base_url=reverse('account_history'),
            querystring=query_dictionary.urlencode()
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['transactions'].number, 1)
