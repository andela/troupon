from django.db import models
from django.contrib.auth.models import User
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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=100, null=False, blank=False, default='')
    last_name = models.CharField(max_length=100, null=False, blank=False, default='')
    user_state = models.SmallIntegerField(choices=STATE_CHOICES,
                                          default=25)

    interest = models.TextField(blank=True, default='')

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


