# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models
import deals.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('slug', models.SlugField(blank=True)),
                ('address', models.CharField(default=b'', max_length=200)),
                ('country', models.SmallIntegerField(default=2, choices=[(1, b'Nigeria'), (2, b'Kenya')])),
                ('location', models.SmallIntegerField(default=47, choices=[(38, b'Mombasa'), (39, b'Kwale'), (40, b'Kilifi'), (41, b'Tana River'), (42, b'Lamu'), (43, b'Taita-Taveta'), (44, b'Garissa'), (45, b'Wajir'), (46, b'Mandera'), (47, b'Marsabit'), (48, b'Isiolo'), (49, b'Meru'), (50, b'Tharaka-Nithi'), (51, b'Embu'), (52, b'Kitui'), (53, b'Machakos'), (54, b'Makueni'), (55, b'Nyandarua'), (56, b'Nyeri'), (57, b'Kirinyaga'), (58, b"Murang'a"), (59, b'Kiambu'), (60, b'Turkana'), (61, b'West Pokot'), (62, b'Samburu'), (63, b'Trans-Nzoia'), (64, b'Uasin Gishu'), (65, b'Elgeyo-Marakwet'), (66, b'Nandi'), (67, b'Baringo'), (68, b'Laikipia'), (69, b'Nakuru'), (70, b'Narok'), (71, b'Kajiado'), (72, b'Kericho'), (73, b'Bomet'), (74, b'Kakamega'), (75, b'Vihiga'), (76, b'Bungoma'), (77, b'Busia'), (78, b'Siaya'), (79, b'Kisumu'), (80, b'Homa Bay'), (81, b'Migori'), (82, b'Kisii'), (83, b'Nyamira'), (84, b'Nairobi')])),
                ('telephone', models.CharField(default=b'', max_length=60)),
                ('email', models.EmailField(default=b'', max_length=254)),
            ],
            bases=(deals.models.ImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
            bases=(deals.models.ImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('original_price', models.IntegerField()),
                ('quorum', models.IntegerField(null=True, blank=True)),
                ('disclaimer', models.TextField(default=b'', blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('country', models.SmallIntegerField(default=2, choices=[(1, b'Nigeria'), (2, b'Kenya')])),
                ('location', models.SmallIntegerField(default=84, choices=[(1, b'Abia'), (2, b'Abuja'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara'), (38, b'Mombasa'), (39, b'Kwale'), (40, b'Kilifi'), (41, b'Tana River'), (42, b'Lamu'), (43, b'Taita-Taveta'), (44, b'Garissa'), (45, b'Wajir'), (46, b'Mandera'), (47, b'Marsabit'), (48, b'Isiolo'), (49, b'Meru'), (50, b'Tharaka-Nithi'), (51, b'Embu'), (52, b'Kitui'), (53, b'Machakos'), (54, b'Makueni'), (55, b'Nyandarua'), (56, b'Nyeri'), (57, b'Kirinyaga'), (58, b"Murang'a"), (59, b'Kiambu'), (60, b'Turkana'), (61, b'West Pokot'), (62, b'Samburu'), (63, b'Trans-Nzoia'), (64, b'Uasin Gishu'), (65, b'Elgeyo-Marakwet'), (66, b'Nandi'), (67, b'Baringo'), (68, b'Laikipia'), (69, b'Nakuru'), (70, b'Narok'), (71, b'Kajiado'), (72, b'Kericho'), (73, b'Bomet'), (74, b'Kakamega'), (75, b'Vihiga'), (76, b'Bungoma'), (77, b'Busia'), (78, b'Siaya'), (79, b'Kisumu'), (80, b'Homa Bay'), (81, b'Migori'), (82, b'Kisii'), (83, b'Nyamira'), (84, b'Nairobi')])),
                ('address', models.CharField(default=b'', max_length=100)),
                ('currency', models.SmallIntegerField(default=1, choices=[(1, b'N'), (2, b'$'), (3, b'KES')])),
                ('image', cloudinary.models.CloudinaryField(default=b'img/photo_default.png', max_length=255, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('max_quantity_available', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_last_modified', models.DateField(auto_now=True)),
                ('date_end', models.DateField(null=True, blank=True)),
                ('advertiser', models.ForeignKey(to='deals.Advertiser')),
                ('category', models.ForeignKey(to='deals.Category')),
            ],
        ),
    ]
