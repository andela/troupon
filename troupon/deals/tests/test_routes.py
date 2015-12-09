from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from deals.models import Deal, Advertiser, Category
from django.core.files import File
from django.template.defaultfilters import slugify
from deals.views import HomePageView, DealsView, DealView,\
                        FilteredDealsView
from faker import Faker
import mock
import cloudinary


def set_advertiser_and_category():
    """Sets the advertiser and category.
    returns a deal dictionary"""
    advertiser = Advertiser(name="XYZ Stores", slug="xyz-stores")
    advertiser.save()
    category = Category(name="Comic Books", slug="comic-books")
    category.save()

    return dict(
        title="Deal #1", description="Deal some...deal all!",
        disclaimer="Deal at your own risk", advertiser=advertiser,
        address="14, Alara Street", state=14,
        slug=slugify("Deal #1"), category=category,
        original_price=1500, price=750,
        duration=15, active=1,
        max_quantity_available=3,
    )


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


class FilteredDealsViewTestCase(TestCase):
    """
    Testcase for routing to the filtered deals view:
    """
    def setUp(self):
        self.deal = set_advertiser_and_category()

    def test_filter_deals_by_category(self):
        """
        test that route to get deals by category works.
        """
        response = self.client.get(
            reverse('deal-filter-with-slug', kwargs={
                'filter_type': 'category',
                'filter_slug': 'comic-books'
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__,
            FilteredDealsView.as_view().__name__
        )

    def test_filter_deals_by_city(self):
        """
        test that route to get deals by city works.
        """
        response = self.client.get(
            reverse('deal-filter-with-slug', kwargs={
                'filter_type': 'city',
                'filter_slug': 'akwa-ibom'
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__,
            FilteredDealsView.as_view().__name__
        )

    def test_filter_deals_by_merchant(self):
        """
        test that route to get deals by merchant works.
        """
        response = self.client.get(
            reverse('deal-filter-with-slug', kwargs={
                'filter_type': 'merchant',
                'filter_slug': 'xyz-stores'
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func.__name__,
            FilteredDealsView.as_view().__name__
        )

    def test_wrong_filter_type_returns_bad_request_error(self):
        """
        test that route to get deals with an invalid
        filter_type errors out.
        """
        response = self.client.get(
            reverse('deal-filter-with-slug', kwargs={
                'filter_type': 'awoof',
                'filter_slug': 'xyz-stores'
            })
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.resolver_match.func.__name__,
            FilteredDealsView.as_view().__name__
        )


class DealViewTestCase(TestCase):

    """This contains tests to check that a HTTP GET
        request for a deal is successful
    """
    def setUp(self):
        self.deal = set_advertiser_and_category()

    def test_deal404_and_single_deal_view(self):
        response = self.client.get(reverse('deal', args=[2000]))
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
        self.deal = set_advertiser_and_category()

    def test_can_view_deal_by_slug(self):
        deal = Deal(**self.deal)
        deal.save()
        response = self.client.get(
            "/deals/{0}/".format(deal.slug)
        )
        self.assertEqual(response.status_code, 200)
