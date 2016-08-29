from django.contrib.auth.models import User
from django.db import models


class UserShippingDetails(models.Model):

    user = models.ForeignKey(User)
    street = models.CharField(max_length=250)
    postal = models.IntegerField()
    state = models.CharField(max_length=250)
    telephone = models.IntegerField()

    def __unicode__(self):
        return u'User %s with username %s' % (
            self.name,
            self.userprofile.user.username
        )
