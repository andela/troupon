# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0009_auto_20151020_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 21, 10, 47, 58, 63063, tzinfo=utc)),
        ),
    ]
