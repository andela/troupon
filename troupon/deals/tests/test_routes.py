from django.test import TestCase
from django.core.urlresolvers import reverse


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

    def test_single_deal_view(self):
        response = self.client.get('/deals/1')
        self.assertEqual(response.status_code, 200)
