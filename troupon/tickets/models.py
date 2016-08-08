from django.db import models
from django.contrib.auth.models import User
from deals.models import Advertiser, Deal


class Ticket(models.Model):
    """
    Stores all unique codes generated for tickets
    """
    user = models.ForeignKey(User)
    item = models.ForeignKey('deals.Deal')
    advertiser = models.ForeignKey('deals.Advertiser')
    ticket_id = models.CharField(max_length=40,
                                 null=False,
                                 blank=False)
    date_created = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
