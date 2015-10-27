# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0007_auto_20151014_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 14, 15, 15, 8, 134613, tzinfo=utc)),
        ),
    ]
