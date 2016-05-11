from django.db import models
from django.contrib.auth.models import User
from deals.models import Advertiser, Deal


class TransactionHistory(models.Model):
    """
    stores details of every charge on stripe
    """
    transaction_id = models.CharField(max_length=100,
                                      null=False,
                                      blank=False,
                                      default='')
    transaction_status = models.CharField(max_length=100,
                                          null=False,
                                          blank=False,
                                          default='')
    transaction_amount = models.IntegerField()
    transaction_created = models.IntegerField()
    transaction_currency = models.CharField(max_length=3,
                                            null=False,
                                            blank=False,
                                            default='')
    failure_code = models.IntegerField(null=True,
                                       blank=True)
    failure_message = models.CharField(max_length=200,
                                       null=True,
                                       blank=True)
    user = models.ForeignKey(User)


class Purchases(models.Model):
    PAYMENT_STATUS = [(1, 'Succeeded'), (2, 'Failed')]
    item = models.ForeignKey('deals.Deal')
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    advertiser = models.ForeignKey('deals.Advertiser')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, default='')
    stripe_transaction_id = models.CharField(max_length=100,
                                      null=False,
                                      blank=False,
                                      default='')
    stripe_transaction_status = models.CharField(max_length=100,
                                          null=False,
                                          blank=False,
                                          default=2,
                                          choices=PAYMENT_STATUS)

    def __str__(self):
        return self.title
