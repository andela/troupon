# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('address', models.CharField(default=b'', max_length=200)),
                ('state', models.SmallIntegerField(default=25, choices=[(1, b'Abia'), (2, b'Abuja Capital Territory'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')])),
                ('telephone', models.CharField(default=b'', max_length=60)),
                ('email', models.EmailField(default=b'', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'', blank=True)),
                ('disclaimer', models.TextField(default=b'', blank=True)),
                ('deal_address', models.CharField(default=b'', max_length=100)),
                ('deal_state', models.SmallIntegerField(default=25, choices=[(1, b'Abia'), (2, b'Abuja Capital Territory'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')])),
                ('original_price', models.IntegerField()),
                ('deal_price', models.IntegerField()),
                ('deal_duration', models.IntegerField()),
                ('deal_active', models.BooleanField(default=False)),
                ('max_quantity_available', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_last_modified', models.DateField(auto_now=True)),
                ('date_end', models.DateField(default=datetime.datetime(2015, 9, 15, 11, 54, 33, 924321, tzinfo=utc))),
                ('advertiser', models.ForeignKey(to='deals.Advertiser')),
                ('category', models.ForeignKey(to='deals.Category')),
            ],
        ),
    ]
