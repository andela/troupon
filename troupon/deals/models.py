from django.db import models
from django.utils import timezone

# Create your models here.
STATE_CHOICES = [
                    (1, 'Abia'),
                    (2, 'Abuja Capital Territory'),
                    (3, 'Adamawa'),
                    (4, 'Akwa Ibom'),
                    (5, 'Anambra'),
                    (6, 'Bauchi'),
                    (7, 'Bayelsa'),
                    (8, 'Benue'),
                    (9, 'Borno'),
                    (10, 'Cross River'),
                    (11, 'Delta'),
                    (12, 'Ebonyi'),
                    (13, 'Edo'),
                    (14, 'Ekiti'),
                    (15, 'Enugu'),
                    (16, 'Gombe'),
                    (17, 'Imo'),
                    (18, 'Jigawa'),
                    (19, 'Kaduna'),
                    (20, 'Kano'),
                    (21, 'Katsina'),
                    (22, 'Kebbi'),
                    (23, 'Kogi'),
                    (24, 'Kwara'),
                    (25, 'Lagos'),
                    (26, 'Nassarawa'),
                    (27, 'Niger'),
                    (28, 'Ogun'),
                    (29, 'Ondo'),
                    (30, 'Osun'),
                    (31, 'Oyo'),
                    (32, 'Plateau'),
                    (33, 'Rivers'),
                    (34, 'Sokoto'),
                    (35, 'Taraba'),
                    (36, 'Yobe'),
                    (37, 'Zamfara'),
              ]  # States in Nigeria


class Deal(models.Model):
    """
        Deals within the troupon system are represented by this
        model.

        title, deal_address, advertiser and category are required.
        Other fields are optional.
    """
    title = models.CharField(max_length=100,
                             null=False,
                             blank=False,
                             default='')
    description = models.TextField(blank=True, default='')
    disclaimer = models.TextField(blank=True, default='')
    advertiser = models.ForeignKey('Advertiser')
    deal_address = models.CharField(max_length=100, blank=False, default='')
    deal_state = models.SmallIntegerField(choices=STATE_CHOICES,
                                          default=25)
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

    def __str__(self):
        return "{0}, {1}, {2}".format(self.id,
                                      self.title,
                                      self.advertiser.name)


class Advertiser(models.Model):
    """Advertisers within the troupon system are represented by this
        model.

        name is required. Other fields are optional.
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            default='')
    address = models.CharField(max_length=200, default='')
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=25)
    telephone = models.CharField(max_length=60, default='')
    email = models.EmailField(default='')

    def __str__(self):
        return "{0}".format(self.name)


class Category(models.Model):
    """
        Categories of deal within the troupon system are represented by
        this model.

        name is required.
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            default='')
