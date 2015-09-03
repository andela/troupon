from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

# Create your models here.
class Account(AbstractUser):
    email = models.EmailField(max_length=254,unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email


