# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0007_auto_20151001_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='image',
            new_name='photo_url',
        ),
        migrations.AlterField(
            model_name='deal',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2015, 10, 2, 3, 47, 50, 570792, tzinfo=utc)),
        ),
    ]
