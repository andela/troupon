from django.db import models
from deals.models import Advertiser
from account.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection
import jsonfield
import json

class Merchant(Advertiser):

    userprofile = models.OneToOneField(UserProfile)
    intlnumber = models.CharField(blank=True, default='', max_length=20)
    enabled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    trusted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Merchant %s with username %s' % (
            self.name, self.userprofile.user.username
        )


class MyJSONField(jsonfield.JSONField):
    """
    A custom JSON field
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE']\
         == 'django.db.backends.postgresql_psycopg2':
            return 'jsonb'
        else:
            return 'text'


class Order(models.Model):
    """
    A model that abstracts an order that consists of one or more
    deals/product
    """
    cart = MyJSONField()
    status = models.BooleanField(default=False,)
    total_cost = models.IntegerField(blank=False,)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return json.dumps(self.cart)

    @classmethod
    def get_all_for_merchant(cls, merchant_id):
        """
        Get orders for a merchant
        """
        query = """
        SELECT * FROM merchant_order
         WHERE cart::jsonb @> '[{"merchant_id":"%s"}]'
        """ % (merchant_id)

        cursor = connection.cursor()
        cursor.execute(query)

        return Order.dictfetchall(cursor)

    @classmethod
    def get_deals_for_merchant(cls, merchant_id, deal_id):
        """
        Get orders for a specific deal put up by a merchant
        """
        query = """
        SELECT * FROM merchant_order
         WHERE cart::jsonb @> '[{"merchant_id":"%s", "deal_id":"%s"}]'
        """ % (merchant_id, deal_id)

        cursor = connection.cursor()
        cursor.execute(query)

        return Order.dictfetchall(cursor)

    @classmethod
    def dictfetchall(cls, cursor):
        """Return all rows from a cursor as a dict"""
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class Sales(models.Model):
    """
    A model that abstracts sales of a deal/product
    """
    user = models.ForeignKey(User)
    deal = models.ForeignKey('deals.Deal')
    date_purchased = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    merchant = models.ForeignKey('merchant.Merchant')
    cost = models.IntegerField()
