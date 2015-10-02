# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_auto_20150928_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='image',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 1, 19, 37, 4, 884382, tzinfo=utc)),
        ),
    ]
