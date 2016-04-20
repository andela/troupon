# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import merchant.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('advertiser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='deals.Advertiser')),
                ('intlnumber', models.CharField(default=b'', max_length=20, blank=True)),
                ('enabled', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('trusted', models.BooleanField(default=False)),
                ('userprofile', models.OneToOneField(to='account.UserProfile')),
            ],
            bases=('deals.advertiser',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cart', merchant.models.MyJSONField(default=dict)),
                ('status', models.BooleanField(default=False)),
                ('total_cost', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_purchased', models.DateField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('deal', models.ForeignKey(to='deals.Deal')),
                ('merchant', models.ForeignKey(to='merchant.Merchant')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
