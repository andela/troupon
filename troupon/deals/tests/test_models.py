from django.test import TestCase
from deals.models import Deal, Advertiser, Category


class DealModelTestCase(TestCase):

    def setUp(self):
        advertiser, category = Advertiser(name="XYZ Stores"), \
                                Category(name="Books")
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

    def test_can_create_read_update_delete_deal(self):
        # create a deal record
        deal = Deal(**self.deal)
        deal.save()
        self.assertIsNotNone(deal.id, None)

        # test a deal record has been added
        deal = Deal.objects.get(id=deal.id)
        self.assertIsNotNone(deal.id)

        # update a deal record
        new_deal_title = 'Deal #2'
        deal = Deal.objects.get(id=deal.id)
        deal.title = new_deal_title
        deal.save()
        self.deal['title'] = new_deal_title  # Update deal title for next test
        self.assertEquals(deal.title, new_deal_title)

        # delete a deal record
        deal = Deal.objects.get(id=deal.id)
        Deal.delete(deal)
        with self.assertRaises(Deal.DoesNotExist) as context:
            Deal.objects.get(**self.deal)
        self.assertTrue("does not exist" in context.exception.message)
