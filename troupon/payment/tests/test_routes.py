from carton.cart import Cart
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.template.defaultfilters import slugify
from django.test import Client, TestCase

from deals.models import Advertiser, Category, Deal


def set_dependent_classes():
    """
    Sets the advertiser, category, deal and user
    and returns a ticket dictionary
    """
    advertiser = Advertiser.objects.create(
        name="XYZ Stores",
        slug="xyz-stores"
    )
    category = Category.objects.create(
        name="Comic Books",
        slug="comic-books"
    )
    deal = Deal.objects.create(
        title="Deal #1", description="Deal some...deal all!",
        disclaimer="Deal at your own risk", advertiser=advertiser,
        address="14, Alara Street", country=1,
        location=25, slug=slugify("Deal #1"), category=category,
        original_price=1500, price=750,
        duration=15, active=1,
        max_quantity_available=3,
    )
    user = User.objects.create_user(
        username="test_user",
        email="test_user@test.com",
        password="test123"
    )

    return dict(
        user=user, item=deal, quantity=1,
        advertiser=advertiser, ticket_id="98329u093ru032r"
    )


class PaymentStatusViewTestCase(TestCase):
    """Test suite for payment's app Payment status view"""

    def setUp(self):
        self.client = Client()
        self.ticket = set_dependent_classes()
        self.client.login(username="test_user", password="test123")
        session = self.client.session
        cart = Cart(session)
        cart.add(self.ticket['item'], price=self.ticket['item'].price)
        session.save()

    def test_get_payment_status_view_returns_200(self):
        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update(
            {
                'status': 'complete'
            }
        )
        url = '{base_url}?{querystring}'.format(
            base_url=reverse('payment_status'),
            querystring=query_dictionary.urlencode()
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
