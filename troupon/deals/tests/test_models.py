from django.test import TestCase
from deals.models import Deal, Advertiser, Category


class DealModelTestCase(TestCase):

    def setUp(self):
        advertiser, category = Advertiser(1), Category(1)
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

    def test_can_create_read_update_delete_deal(self):
        # create a deal record
        deal = Deal(**self.deal)
        deal.save()
        self.assertIsNotNone(deal.id, None)

        # test a deal record has been added
        deal = Deal.objects.get(**self.deal)
        self.assertIsNotNone(deal.id)

        # update a deal record
        new_deal_title = 'Deal #2'
        deal = Deal.objects.get(**self.deal)
        deal.title = new_deal_title
        deal.save()
        self.deal['title'] = new_deal_title  # Update deal title for next test
        self.assertEquals(deal.title, new_deal_title)

        # delete a deal record
        deal = Deal.objects.get(**self.deal)
        Deal.delete(deal)
        with self.assertRaises(Deal.DoesNotExist) as context:
            Deal.objects.get(**self.deal)
        self.assertTrue("does not exist" in context.exception.message)
