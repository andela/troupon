"""Model defined for UserProfile creation."""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from deals.models import COUNTRY_CHOICES, ALL_LOCATIONS


class UserProfile(models.Model):
    """Class that defines user profile model.

    Attributes: user,
                country,
                location,
                occupation,
                phonenumber,
                intlnumber.
    """

    user = models.OneToOneField(User)
    country = models.SmallIntegerField(choices=COUNTRY_CHOICES, default=2)
    location = models.SmallIntegerField(choices=ALL_LOCATIONS, default=84)
    occupation = models.TextField(blank=True, default='')
    phonenumber = models.CharField(blank=True, default='', max_length=20)
    intlnumber = models.CharField(blank=True, default='', max_length=20)

    def check_diff(self, request_value):
        """Check for differences between request and model data.

            Args:
                request_value: form data passed in from post method.
            Returns:
                A dictionary containing user information in unicode format.
        """
        for field in request_value:
            if getattr(self, field, False) != False \
                and getattr(self, field) != request_value[field] and \
                    request_value[field] != '':
                    setattr(self, field, request_value[field])
        self.save()
        return {
            u'country': self.country,
            u'location': self.location,
            u'phonenumber': self.phonenumber,
            u'intlnumber': self.intlnumber,
            u'occupation': self.occupation
        }

    def is_complete(self):
        """Checks if a user's profile is completed"""
        for field in self._meta.get_all_field_names():
            try:
                fieldattr = getattr(self, field)
                if fieldattr == '':
                    return False
                if type(fieldattr) == User:
                    if fieldattr.first_name == '' or fieldattr.last_name == '':
                        return False
            except:
                pass
        return True

    def is_approved_merchant(self):
        """Checks if the user is an approved merchant"""
        try:
            return getattr(self.merchant, 'approved', False)
        except:
            return False

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    """Creates the user profile for a given User instance.

    Args: sender, instance, created,
       Sender: The model class,
       Instance: The actual instance being saved,
       Created: Boolean that defaults to True if user is created
    """
    if created:
        UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User,
                      dispatch_uid=create_user_profile)
