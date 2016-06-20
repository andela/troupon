# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_auto_20160523_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='country',
            field=models.SmallIntegerField(default=1, choices=[(1, b'Nigeria'), (2, b'Kenya')]),
        ),
    ]
