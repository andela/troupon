# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(default=b'', max_length=100)),
                ('transaction_status', models.CharField(default=b'', max_length=100)),
                ('transaction_amount', models.IntegerField()),
                ('transaction_created', models.IntegerField()),
                ('transaction_currency', models.CharField(default=b'', max_length=3)),
                ('failure_code', models.IntegerField(null=True, blank=True)),
                ('failure_message', models.CharField(max_length=200, null=True, blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
