from django.db import models
from deals.models import Advertiser
from account.models import UserProfile


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
