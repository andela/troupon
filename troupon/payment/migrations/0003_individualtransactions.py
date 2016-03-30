# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0001_initial'),
        ('payment', '0002_auto_20160309_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default=b'', blank=True)),
                ('transaction_id', models.CharField(default=b'', max_length=100)),
                ('transaction_status', models.CharField(default=b'', max_length=100)),
                ('merchant_id', models.ForeignKey(to='merchant.Merchant')),
            ],
        ),
    ]
