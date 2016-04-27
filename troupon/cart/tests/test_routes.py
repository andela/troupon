from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from deals.models import Deal
from deals.tests.test_routes import set_advertiser_and_category


class AddToCartRouteTestCase(TestCase):
    """Tests view cart route."""

    def setUp(self):
        self.client = Client()

    def test_add_cart_items(self):
        """Test post cart items"""
        data = {
            "dealid": 1
        }
        response = self.client.post(reverse('add'), data)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        del self.client


class ViewCartRouteTestCase(TestCase):
    """Tests view cart route."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'testuser1', 'testuser1@mail.com', '12345'
        )
        deal = set_advertiser_and_category()
        self.deal = Deal(**deal)
        self.deal.save()

    def test_get_cart_items(self):
        response = self.client.post(
            reverse('login'),
            dict(username='testuser1@mail.com', password='12345')
        )

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        data = {
            "dealid": 1
        }
        res = self.client.post(reverse('add'), data)
        self.assertEqual(res.status_code, 302)
        cart_response = self.client.get(reverse('view'))
        self.assertEqual(cart_response.status_code, 200)

    def tearDown(self):
        del self.client


class CheckoutPageTestCase(TestCase):
    """Test checkout route."""

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        del self.client


class ClearCartViewRouteTestCase(TestCase):
    """Test clear cart view route."""

    def setUp(self):
        self.client = Client()

    def test_get_clear_cart(self):
        data = {
            "dealid": 1
        }
        response = self.client.post(reverse('add'), data)
        self.assertEqual(response.status_code, 302)

        clear_response = self.client.get(reverse('clear'))
        self.assertEqual(clear_response.status_code, 302)

    def tearDown(self):
        del self.client


class RemoveItemViewRouteTestCase(TestCase):
    """Test remove item view route."""

    def setUp(self):
        self.client = Client()

    def test_get_remove_cart(self):
        data = {
            "dealid": 1
        }
        response = self.client.post(reverse('add'), data)
        self.assertEqual(response.status_code, 302)

        remove_response = self.client.post(reverse('remove'), data)
        self.assertEqual(remove_response.status_code, 302)

    def tearDown(self):
        del self.client
