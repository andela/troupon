from django.contrib.auth.models import User
from django.test import TestCase

from deals.models import Advertiser, Category, Deal
from tickets.models import Ticket


class TicketModelTestCase(TestCase):
    """Testsuite for the Tickets model"""

    def setUp(self):
        advertiser = Advertiser(name="XYZ Stores")
        advertiser.save()
        category = Category(name="Books")
        category.save()
        deal = Deal(title="Deal #1",
                    description="Deal some...deal all!",
                    disclaimer="Deal at your own risk",
                    advertiser=advertiser,
                    address="14, Alara Street",
                    country=1,
                    location=25,
                    category=category,
                    original_price=1500,
                    price=750,
                    duration=15,
                    active=1,
                    max_quantity_available=3,
                    featured=True,
                    )
        deal.save()
        user = User(username="test_user", password="test123")
        user.save()
        self.ticket = dict(
            user=user, item=deal, quantity=1,
            advertiser=advertiser, ticket_id="98329u093ru032r"
        )

    def test_can_create_read_update_ticket(self):
        # create a deal record
        ticket = Ticket(**self.ticket)
        ticket.save()
        self.assertIsNotNone(ticket.id, None)

        # test that a ticket record has been added
        ticket = Ticket.objects.get(id=ticket.id)
        self.assertIsNotNone(ticket.id)

        # update a ticket record
        new_ticket_id = "898273499823hiuh32898w"
        ticket = Ticket.objects.get(id=ticket.id)
        ticket.ticket_id = new_ticket_id
        ticket.save()

        # update deal title for next test
        self.ticket['ticket_id'] = new_ticket_id
        self.assertEquals(ticket.ticket_id, new_ticket_id)

        # delete a ticket record
        ticket = Ticket.objects.get(id=ticket.id)
        Ticket.delete(ticket)
        with self.assertRaises(Ticket.DoesNotExist) as context:
            Ticket.objects.get(**self.ticket)
        self.assertTrue("does not exist" in context.exception.message)
