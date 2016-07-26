# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_advertiser_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertiser',
            name='logo',
        ),
    ]
