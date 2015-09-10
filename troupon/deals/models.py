from django.db import models
from django.utils import timezone

# Create your models here.
STATE_CHOICES = [(1, 'abia'),
                 (2, 'adamawa'),
                 (3, 'akwa-ibom'),
                 (4, 'anambra'),
                 (5, 'bauchi'),
                 (14, 'lagos'),
                 ]


class Deal(models.Model):
    title = models.CharField(max_length=100,
                             null=False,
                             blank=False,
                             default='')
    description = models.TextField(blank=True, default='')
    disclaimer = models.TextField(blank=True, default='')
    advertiser = models.ForeignKey('Advertiser')
    deal_address = models.CharField(max_length=100, blank=False, default='')
    deal_state = models.SmallIntegerField(choices=STATE_CHOICES,
                                          default=14)
    category = models.ForeignKey('Category')
    original_price = models.IntegerField()
    deal_price = models.IntegerField()
    deal_duration = models.IntegerField()
    deal_active = models.BooleanField(default=False)
    max_quantity_available = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    date_end = models.DateField(default=timezone.now())


class Advertiser(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=200)
    state = models.SmallIntegerField(choices=STATE_CHOICES)
    telephone = models.CharField(max_length=60)
    email = models.EmailField()


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
