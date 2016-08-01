# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0004_advertiser_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='type',
            field=models.SmallIntegerField(default=1, choices=[(1, b'Physical'), (2, b'Virtual')]),
        ),
        migrations.AlterField(
            model_name='advertiser',
            name='logo',
            field=cloudinary.models.CloudinaryField(default=b'img/logo-v-lg.png', max_length=255, blank=True),
        ),
    ]
