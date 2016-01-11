from django.db import models
from django.contrib.auth.models import User


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
