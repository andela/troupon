# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0011_auto_20151021_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 21, 15, 57, 29, 483361, tzinfo=utc)),
        ),
    ]
