from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from deals.models import Deal, Advertiser, Category
from django.core.files import File
from django.template.defaultfilters import slugify
from deals.views import HomePageView, DealsView, DealView
from faker import Faker
import mock
import cloudinary


def set_advertiser_and_category():
    """Sets the advertiser and category.
    returns a deal dictionary"""
    advertiser = Advertiser(name="XYZ Stores", slug="xyz-stores")
    advertiser.save()
    category = Category(name="Books", slug="books")
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


class DealCategoryViewTestCase(TestCase):

    def setUp(self):
        self.deal = set_advertiser_and_category()

    def test_can_view_deals_by_category(self):
        deal = Deal(**self.deal)
        deal.save()
        response = self.client.get("/deals/category/books/")
        self.assertEqual(response.status_code, 200)


class CategoriesViewTestCase(TestCase):

    def setUp(self):
        fake = Faker()
        for _ in range(0, 10):
            fake_word = fake.word()
            category = Category(
                name=str(fake_word),
                slug=str(fake.slug(unicode(fake_word))))
            category.save()

    def test_can_view_categories(self):
        response = self.client.get('/deals/categories/')
        self.assertEqual(response.status_code, 200)


class AdvertisersViewTestCase(TestCase):
    
    def setUp(self):
        self.deal = set_advertiser_and_category()
        deal = Deal(**self.deal)
        deal.save()
    
    def test_can_view_advertisers(self):
        print "-->>>>>{}".format(Advertiser.objects.all())
        response = self.client.get(reverse("deal-advertisers"))
        self.assertEqual(response.status_code, 200)

    def test_can_view_deals_by_advertiser(self):
        response = self.client.get(
            "/deals/merchant/{0}/".format(slugify('XYZ Stores')))
        self.assertEqual(response.status_code, 200)

class StatesViewTestCase(TestCase):
    pass