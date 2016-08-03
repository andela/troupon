from datetime import date
from random import randint
import re

from cloudinary.models import CloudinaryField
from django.db import models
from django.core import signals
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import pre_save
from troupon.settings.base import SITE_IMAGES

# Country Choices
COUNTRY_CHOICES = [(1, 'Nigeria'), (2, 'Kenya')]

# States in Nigeria
NIGERIAN_LOCATIONS = [
    (1, 'Abia'), (2, 'Abuja'), (3, 'Adamawa'),
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

# Counties in Kenya
KENYAN_LOCATIONS = [
    (38, 'Mombasa'), (39, 'Kwale'), (40, 'Kilifi'),
    (41, 'Tana River'), (42, 'Lamu'), (43, 'Taita-Taveta'),
    (44, 'Garissa'), (45, 'Wajir'), (46, 'Mandera'),
    (47, 'Marsabit'), (48, 'Isiolo'), (49, 'Meru'),
    (50, 'Tharaka-Nithi'), (51, 'Embu'), (52, 'Kitui'),
    (53, 'Machakos'), (54, 'Makueni'), (55, 'Nyandarua'),
    (56, 'Nyeri'), (57, 'Kirinyaga'), (58, "Murang'a"),
    (59, 'Kiambu'), (60, 'Turkana'), (61, 'West Pokot'),
    (62, 'Samburu'), (63, 'Trans-Nzoia'), (64, 'Uasin Gishu'),
    (65, 'Elgeyo-Marakwet'), (66, 'Nandi'), (67, 'Baringo'),
    (68, 'Laikipia'), (69, 'Nakuru'), (70, 'Narok'),
    (71, 'Kajiado'), (72, 'Kericho'), (73, 'Bomet'),
    (74, 'Kakamega'), (75, 'Vihiga'), (76, 'Bungoma'),
    (77, 'Busia'), (78, 'Siaya'), (79, 'Kisumu'),
    (80, 'Homa Bay'), (81, 'Migori'), (82, 'Kisii'),
    (83, 'Nyamira'), (84, 'Nairobi')
]

ALL_LOCATIONS = NIGERIAN_LOCATIONS + KENYAN_LOCATIONS

# Available site-wide currencies
CURRENCY_CHOICES = [
    (1, 'N'),
    (2, '$'),
    (3, 'KES'),
]

# Date sorting epochs:
EPOCH_CHOICES = [
    (1, '1 day'),
    (7, 'Last 7 Days'),
    (14, 'Last 2 Weeks'),
    (30, '1 Month'),
    (-1, 'Show All'),
]

# Rating choices when reviewing a deal
RATING_CHOICES = [
    (1, '1 star'),
    (2, '2 star'),
    (3, '3 star'),
    (4, '4 star'),
    (5, '5 star'),
]

# Category of deal as either physical or virtual
DEAL_TYPES = [(1, 'Physical'), (2, 'Virtual')]

class Deal(models.Model):
    """Deals within the troupon system are represented by this
        model.

        title, deal_address, advertiser and category are required.
        Other fields are optional.
    """

    price = models.IntegerField()
    duration = models.IntegerField()
    original_price = models.IntegerField()
    category = models.ForeignKey('Category')
    advertiser = models.ForeignKey('Advertiser')
    quorum = models.IntegerField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(blank=True, null=False, unique=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    country = models.SmallIntegerField(choices=COUNTRY_CHOICES, default=2)
    location = models.SmallIntegerField(choices=ALL_LOCATIONS, default=84)
    address = models.CharField(max_length=100, blank=False, default='')
    currency = models.SmallIntegerField(choices=CURRENCY_CHOICES, default=1)
    image = CloudinaryField(
        resource_type='image',
        type='upload',
        blank=True,
        default="img/photo_default.png"
    )
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    max_quantity_available = models.IntegerField()
    type = models.SmallIntegerField(choices=DEAL_TYPES, default=1)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    date_end = models.DateField(blank=True, null=True)

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

    def state_name(self):
        """Returns the state name
        """
        if self.country == 1:
            return dict(NIGERIAN_LOCATIONS).get(self.state)
        else:
            return dict(KENYAN_LOCATIONS).get(self.state)

    def slideshow_image_url(self):
        """Returns a slide image URL
        """
        image_url = self.image.build_url(
            width=SITE_IMAGES['slideshow_image_width'],
            height=SITE_IMAGES['slideshow_image_height'],
            crop="fit",
        )
        return image_url

    def discount(self):
        """Returns deal discount"""
        discount = 1 - (float(self.price) / self.original_price)
        return "{0:.0%}".format(discount)

    def saving(self):
        """Returns deal saving"""
        saving = self.original_price - self.price
        return saving

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}".format(self.id,
                                                self.title,
                                                self.advertiser.name,
                                                self.price,
                                                self.currency)

    def get_absolute_url(self):
        return "/deals/{}/" .format(self.id)


class ImageMixin(object):
    """Mixes in an image property which is a random image selected from
    all available deals
    """

    def image(self):
        """Retrieve random photo of deal under this category
        """
        deals = Deal.objects.filter(category=self.id)
        if len(deals) is not 0:
            return deals[randint(0, len(deals) - 1)].image.url


class Advertiser(ImageMixin, models.Model):
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
    slug = models.SlugField(blank=True)
    address = models.CharField(max_length=200, default='')
    country = models.SmallIntegerField(choices=COUNTRY_CHOICES, default=2)
    if country == 1:
        location = models.SmallIntegerField(
            choices=NIGERIAN_LOCATIONS, default=25)
    else:
        location = models.SmallIntegerField(
            choices=KENYAN_LOCATIONS, default=47)
    telephone = models.CharField(max_length=60, default='')
    email = models.EmailField(default='')
    logo = CloudinaryField(
        resource_type='image',
        type='upload',
        blank=True,
        default="img/logo-v-lg.png"
    )

    def __str__(self):
        return "{0}".format(self.name)


class Category(ImageMixin, models.Model):
    """Categories of deal within the troupon system are represented by
       this model.

        name is required.
    """
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            default='')
    slug = models.SlugField(blank=True)

    def __str__(self):
        return "{0}".format(self.name)


def set_deal_inactive(**kwargs):
    """Set deal to inactive if the end date set is present date
    """
    date_today = date.today()
    Deal.objects.filter(date_end=date_today.isoformat()).update(active=False)


@receiver(pre_save, sender=Deal)
def set_deal_slug(sender, instance, **kwargs):
    """Set deal slug to one terminated with a timestamp
    """
    if instance._state.adding is True:  # continue if instance is newly created
        date_created = str(timezone.now().date())
        slug = slugify('%s %s' % (instance.title, date_created))

        deal_slug_exists = Deal.objects.filter(
            slug__startswith=slug).order_by('-date_created')

        if deal_slug_exists:
            deal_title_slug = slugify(instance.title)
            deal_title_slug_len = len(deal_title_slug) + 1
            date, counter = re.match(
                '^([\d]{4}-[\d]{2}-[\d]{2})[-]?([\d]{0,})$',
                deal_slug_exists[0].slug[deal_title_slug_len:]).groups()
            radix = len(deal_slug_exists)
            counter = radix if counter == '' else int(counter) + radix
            slug = '{0}-{1}-{2}'.format(
                deal_title_slug, slugify(date_created),
                counter
            )

        instance.slug = slug

signals.request_started.connect(set_deal_inactive)


class Review(models.Model):
    author = models.ForeignKey('auth.User')
    deal = models.ForeignKey(Deal)
    description = models.TextField(max_length=1000)
    rating = models.SmallIntegerField(choices=RATING_CHOICES, default=5)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "ID: {0}, Deal: {1}, Rating: {2}".format(self.id,
                                                        self.deal.title,
                                                        self.rating)

    def ratings_full(self):
        """
        Returns ratings_full variable for displaying ratings
        """
        ratings_full = list(range(1, int(self.rating) + 1))
        return ratings_full

    def ratings_empty(self):
        """
        Returns ratings_empty variable for displaying ratings
        """
        ratings_full = list(range(1, int(self.rating) + 1))
        ratings_empty = list(range(1, 6 - len(ratings_full)))
        return ratings_empty
