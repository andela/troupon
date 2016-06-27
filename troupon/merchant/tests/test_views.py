from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils.importlib import import_module
from django.conf import settings

from accounts.tests.test_routes import UserProfileMerchantTestCase
from deals.tests.test_routes import set_advertiser_and_category
from merchant.views import CreateDealView


class ApprovedMerchantTestCase(UserProfileMerchantTestCase):

    """Testcase for deal creation form and deal creation. """

    def test_merchant_can_view_deal_form(self):

        response = self.client.get(reverse('merchant_create_deal'))
        self.assertEquals(response.status_code, 302)

    def test_merchant_can_create_deal(self):

        deal = set_advertiser_and_category()
        request = self.factory.post(
            reverse('merchant_create_deal'), deal)
        request.user = self.user
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = CreateDealView.as_view()(request)
        self.assertEquals(response.status_code, 302)
