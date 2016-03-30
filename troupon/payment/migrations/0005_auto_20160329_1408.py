# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20160329_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualtransactions',
            name='advertiser',
            field=models.ForeignKey(to='deals.Advertiser'),
        ),
    ]
