from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile


# Create your models here.
class UserShippingDetails(User):

    user = models.OneToOneField(UserProfile)
    street = models.CharField(max_length=250)
    postal = models.IntegerField()
    state = models.CharField(max_length=250)
    telephone = models.IntegerField()

    def __unicode__(self):
        return u'User %s with username %s' % (
            self.name,
            self.userprofile.user.username
        )
