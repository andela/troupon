from django.test import TestCase
from django.core.urlresolvers import reverse
from deals.models import Deal, Advertiser, Category


class HomepageRouteTests(TestCase):
    """docstring for HomepageRouteTests"""

    def test_homepage_returns_200(self,):
        """
        The homepage should return a code of 200
        """

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_can_access_homepage(self,):
        """
        Checks if an anonymous user can view the landing page
        """

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)


class SingleDealViewTestCase(TestCase):
    """
        This contains tests to check that an HTTP GET
        request for a deal is successful
    """
    def setUp(self):
        advertiser, category = Advertiser(name="XYZ Stores"), \
                                Category(name="Books")
        advertiser.save()
        category.save()
        self.deal = dict(title="Deal #1",
                         description="Deal some...deal all!",
                         disclaimer="Deal at your own risk",
                         advertiser=advertiser,
                         deal_address="14, Alara Street",
                         deal_state=14,
                         category=category,
                         original_price=1500,
                         deal_price=750,
                         deal_duration=15,
                         deal_active=1,
                         max_quantity_available=3,
                         latitude=210.025,
                         longitude=250.015,
                         )

    def test_single_deal_view(self):
        response = self.client.get('/deals/1/')
        self.assertEqual(response.status_code, 200)

        deal = Deal(**self.deal)
        deal.save()

        response = self.client.get('/deals/{0}/'.format(deal.id))
        self.assertIn(str(deal.id), response.content)
