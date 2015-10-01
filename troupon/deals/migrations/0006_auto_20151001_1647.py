# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0005_auto_20150928_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 1, 15, 47, 12, 37805, tzinfo=utc)),
        ),
    ]
