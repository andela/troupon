from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from deals.models import Deal, Advertiser, Category
from django.core.files import File
from deals.views import HomePageView, DealsView, DealView
import os
import mock
import cloudinary



class HomepageViewTestCase(TestCase):
    """docstring for HomepageRouteTests"""

    def test_homepage_returns_200(self):
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


class HomepageRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_homepage_route_returns_200(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)

    def test_homepage_route_resolves_to_correct_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(
            response.resolver_match.func.__name__,
            HomePageView.as_view().__name__
        )


class DealsRouteTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_deals_route_returns_200(self):
        response = self.client.get(reverse('deals'))
        self.assertEquals(response.status_code, 200)

    def test_deals_route_resolves_to_correct_view(self):
        response = self.client.get(reverse('deals'))
        self.assertEqual(
            response.resolver_match.func.__name__,
            DealsView.as_view().__name__
        )


class DealViewTestCase(TestCase):

    """This contains tests to check that a HTTP GET
        request for a deal is successful
    """
    def setUp(self):
        advertiser, category = Advertiser(name="XYZ Stores"), \
                                Category(name="Books", slug="books")
        advertiser.save()
        category.save()

        self.deal = dict(title="Deal #1",
                         description="Deal some...deal all!",
                         disclaimer="Deal at your own risk",
                         advertiser=advertiser,
                         address="14, Alara Street",
                         state=14,
                         category=category,
                         original_price=1500,
                         price=750,
                         duration=15,
                         active=1,
                         max_quantity_available=3,
                         latitude=210.025,
                         longitude=250.015,
                         )

    def test_deal404_and_single_deal_view(self):
        response = self.client.get('/deals/1/')
        self.assertEqual(response.status_code, 404)

        deal = Deal(**self.deal)
        deal.save()

        response = self.client.get('/deals/{0}/'.format(deal.id))
        self.assertIn(str(deal.id), response.content)

    @mock.patch('deals.views.DealView.upload', mock.MagicMock(name="upload"))
    @mock.patch('deals.models.Deal.save', mock.MagicMock(name="save"))
    def test_upload_to_cloudinary(self):
        mock_file = mock.MagicMock(spec=File, name='FileMock')
        mock_file.name = 'testimage.jpg'
        self.deal['photo'] = mock_file
        cloudinary.config = mock.MagicMock(name='cloudinary')
        view = DealView.as_view()
        request = RequestFactory().post('/deals', self.deal)
        response = view(request)
        self.assertTrue(DealView.upload.called)
        self.assertEqual(response.status_code, 302)


class DealSlugViewTestCase(TestCase):

    def setUp(self):
        category, advertiser = Category(name="books", slug="books"), \
            Advertiser(name="XYZ Stores")
        category.save()
        advertiser.save()
        self.deal = dict(
            title="deal", description="Deal some...deal all!",
            disclaimer="Deal at your own risk", advertiser=advertiser,
            address="14, Alara Street", state=14, category=category,
            original_price=1500, price=750, duration=15,
            active=1, max_quantity_available=3, latitude=210.025,
            longitude=250.015, slug="deal"
        )

    def test_can_view_deal_by_slug(self):
        deal = Deal(**self.deal)
        deal.save()
        response = self.client.get(
            "/deals/{0}/{1}/".format(deal.id, deal.slug)
        )
        self.assertEqual(response.status_code, 200)


class DealCategoryViewTestCase(TestCase):

    def setUp(self):
        category, advertiser = Category(name="books", slug="books"), \
            Advertiser(name="XYZ Stores")
        category.save()
        advertiser.save()
        self.deal = dict(
            title="Deal #1", description="Deal some...deal all!",
            disclaimer="Deal at your own risk", advertiser=advertiser,
            address="14, Alara Street", state=14, category=category,
            original_price=1500, price=750, duration=15,
            active=1, max_quantity_available=3, latitude=210.025,
            longitude=250.015,
        )

    def test_can_view_deals_by_category(self):
        deal = Deal(**self.deal)
        deal.save()
        response = self.client.get("/deals/listings/?category=books")
        self.assertEqual(response.status_code, 200)
