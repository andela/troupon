# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_auto_20160309_1220'),
        ('payment', '0003_individualtransactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualtransactions',
            name='merchant_id',
        ),
        migrations.AddField(
            model_name='individualtransactions',
            name='advertiser',
            field=models.ForeignKey(default=b'', to='deals.Advertiser'),
        ),
    ]
