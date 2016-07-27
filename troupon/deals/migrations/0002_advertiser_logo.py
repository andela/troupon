# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertiser',
            name='logo',
            field=cloudinary.models.CloudinaryField(default=b'img/default_logo.png', max_length=255, blank=True),
        ),
    ]
