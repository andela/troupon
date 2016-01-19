from django.test import TestCase
from deals.tests.test_routes import set_advertiser_and_category
from merchant.models import Merchant, Order, Sales
from deals.models import Deal
from django.contrib.auth.models import User


class OrderModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        deal = set_advertiser_and_category()
        cls.deal = Deal(**deal)
        cls.deal.save()

        cls.user = User.objects.create_user(
            'testuser1', 'testuser1@mail.com', '12345'
        )

        is_merchant = cls.user.profile.is_approved_merchant()

        if not is_merchant:
            cls.merchant = Merchant(
                advertiser_ptr=cls.deal.advertiser,
                userprofile=cls.user.profile,
                enabled=True,
                approved=True,
                intlnumber='123456789'
            )
            cls.merchant.save()

        super(OrderModelTestCase, cls).setUpClass()

    def test_can_create_order(self):
        """
        Test that order can be created
        """
        order = Order(
            user=self.user,
            total_cost=500,
            status=1,
            cart=[
                {
                    "merchant_id": "{}".format(self.user.profile.merchant.id),
                    "deal_id": self.deal.id,
                    "quantity": 10,
                    "amount": 50,
                }
            ]
        )
        order.save()
        self.assertNotEqual(Order.objects.count(), 0)

    def test_can_retrieve_order_for_a_merchant(self):
        """
        Test that order can be retrieved for a merchant
        """
        Order.objects.create(
            user=self.user,
            total_cost=500,
            status=1,
            cart=[
                {
                    "merchant_id": "{}".format(self.user.profile.merchant.id),
                    "deal_id": self.deal.id,
                    "quantity": 10,
                    "amount": 50,
                }
            ]
        )
        self.assertNotEqual(Order.objects.count(), 0)
        queryset = Order.get_all_for_merchant(self.user.profile.merchant.id)
        self.assertEqual(
            queryset[0]['id'], Order.objects.latest('date_created').id
        )

    def test_can_retrieve_order_for_a_deal_by_a_merchant(self):
        """
        Test that order can be retrieved for a deal put up by a merchant
        """
        Order.objects.create(
            user=self.user,
            total_cost=500,
            status=1,
            cart=[
                {
                    "merchant_id": "{}".format(self.user.profile.merchant.id),
                    "deal_id": self.deal.id,
                    "quantity": 10,
                    "amount": 50
                }
            ]
        )
        self.assertNotEqual(Order.objects.count(), 0)
        queryset = Order.get_deals_for_merchant(
            self.user.profile.merchant.id, self.deal.id)
        self.assertIsNotNone(queryset)

    @classmethod
    def tearDownClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()
        super(OrderModelTestCase, cls).tearDownClass()


class SalesModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        Deal.objects.all().delete()
        User.objects.all().delete()

        deal = set_advertiser_and_category()
        cls.deal = Deal(**deal)
        cls.deal.save()

        cls.user = User.objects.create_user(
            'testuser1', 'testuser1@mail.com', '12345'
        )
        cls.test_merchant = User.objects.create_user(
            'testmerchant1', 'testmerchant1@mail.com', '12345'
        )
        is_merchant = cls.test_merchant.profile.is_approved_merchant()

        if not is_merchant:
            cls.test_merchant = Merchant(
                advertiser_ptr=cls.deal.advertiser,
                userprofile=cls.test_merchant.profile,
                enabled=True,
                approved=True,
                intlnumber='123456789'
            )
            cls.test_merchant.save()

        super(SalesModelTestCase, cls).setUpClass()

    def test_can_create_sales_record(self):
        """
        Test that sale can be created
        """
        Sales.objects.create(
            user=self.user, deal=self.deal, quantity=500,
            merchant=self.test_merchant, cost=8000
        )

        self.assertNotEqual(Sales.objects.count(), 0)

    def test_can_retrieve_order_for_a_merchant(self):
        """
        Test that monthly sale of a deal can be retrieved for a merchant
        """
        Sales.objects.create(
            user=self.user, deal=self.deal, quantity=500,
            merchant=self.test_merchant, cost=8000
        )

        self.assertNotEqual(Sales.objects.count(), 0)

        queryset = Sales.objects.filter(merchant=self.test_merchant)
        self.assertIsNotNone(queryset)
        self.assertIn(Sales.objects.latest('date_purchased'), queryset)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Deal.objects.all().delete()
        super(SalesModelTestCase, cls).tearDownClass()
