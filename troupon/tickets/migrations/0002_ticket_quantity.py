# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
