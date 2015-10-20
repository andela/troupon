from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from troupon.settings.base import SITE_IMAGES

# States in Nigeria
STATE_CHOICES = [
    (1, 'Abia'), (2, 'Abuja Capital Territory'), (3, 'Adamawa'),
    (4, 'Akwa Ibom'), (5, 'Anambra'), (6, 'Bauchi'),
    (7, 'Bayelsa'), (8, 'Benue'), (9, 'Borno'),
    (10, 'Cross River'), (11, 'Delta'), (12, 'Ebonyi'),
    (13, 'Edo'), (14, 'Ekiti'), (15, 'Enugu'),
    (16, 'Gombe'), (17, 'Imo'), (18, 'Jigawa'),
    (19, 'Kaduna'), (20, 'Kano'), (21, 'Katsina'),
    (22, 'Kebbi'), (23, 'Kogi'), (24, 'Kwara'),
    (25, 'Lagos'), (26, 'Nassarawa'), (27, 'Niger'),
    (28, 'Ogun'), (29, 'Ondo'), (30, 'Osun'),
    (31, 'Oyo'), (32, 'Plateau'), (33, 'Rivers'),
    (34, 'Sokoto'), (35, 'Taraba'), (36, 'Yobe'),
    (37, 'Zamfara'),
]

# Available site-wide currencies
CURRENCY_CHOICES = [
    (1, 'N'),
    (2, '$'),
]

# date sorting epochs:
EPOCH_CHOICES = [
    (7, "Last 7 Days"),
    (14, "2 Weeks"),
    (30, "1 Month"),
    (0, "Show All"),
]


class Deal(models.Model):
    """Deals within the troupon system are represented by this
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
    address = models.CharField(max_length=100, blank=False, default='')
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=25)
    currency = models.SmallIntegerField(choices=CURRENCY_CHOICES, default=1)
    category = models.ForeignKey('Category')
    original_price = models.IntegerField()
    price = models.IntegerField()
    duration = models.IntegerField()
    image = CloudinaryField(
        resource_type='image',
        type='upload',
        blank=True, 
        default="img/photo_default.png"
    )
    active = models.BooleanField(default=False)
    max_quantity_available = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    date_end = models.DateField(blank=True)
    featured = models.BooleanField(default=False)

    def currency_symbol(self):
        return CURRENCY_CHOICES[self.currency - 1][1]

    def thumbnail_image_url(self):
        """Returns a thumbnail image URL
        """
        image_url = self.image.build_url(
            width=SITE_IMAGES['thumbnail_image_width'],
            height=SITE_IMAGES['thumbnail_image_height'],
            crop="fit",
        )
        return image_url

    def slideshow_image_url(self):
        """Returns a slide image URL
        """
        image_url = self.image.build_url(
            width=SITE_IMAGES['slideshow_image_width'],
            height=SITE_IMAGES['slideshow_image_height'],
            crop="fit",
        )
        return image_url
    

    

    def __str__(self):
        return "{0}, {1}, {2}".format(self.id,
                                      self.title,
                                      self.advertiser.name)


class Advertiser(models.Model):
    """Advertisers within the troupon system are represented by this
        model.

        name is required. Other fields are optional.
    """
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default=''
    )
    address = models.CharField(max_length=200, default='')
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=25)
    telephone = models.CharField(max_length=60, default='')
    email = models.EmailField(default='')

    def __str__(self):
        return "{0}".format(self.name)


class Category(models.Model):
    """Categories of deal within the troupon system are represented by
       this model.

        name is required.
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            default='')

    def __str__(self):
        return "{0}".format(self.name)
