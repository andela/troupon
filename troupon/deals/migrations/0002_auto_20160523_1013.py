# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertiser',
            name='state',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='state',
        ),
        migrations.AddField(
            model_name='advertiser',
            name='country',
            field=models.SmallIntegerField(default=2, choices=[(1, b'Nigeria'), (2, b'Kenya')]),
        ),
        migrations.AddField(
            model_name='advertiser',
            name='location',
            field=models.SmallIntegerField(default=47, choices=[(1, b'Mombasa'), (2, b'Kwale'), (3, b'Kilifi'), (4, b'Tana River'), (5, b'Lamu'), (6, b'Taita-Taveta'), (7, b'Garissa'), (8, b'Wajir'), (9, b'Mandera'), (10, b'Marsabit'), (11, b'Isiolo'), (12, b'Meru'), (13, b'Tharaka-Nithi'), (14, b'Embu'), (15, b'Kitui'), (16, b'Machakos'), (17, b'Makueni'), (18, b'Nyandarua'), (19, b'Nyeri'), (20, b'Kirinyaga'), (21, b"Murang'a"), (22, b'Kiambu'), (23, b'Turkana'), (24, b'West Pokot'), (25, b'Samburu'), (26, b'Trans-Nzoia'), (27, b'Uasin Gishu'), (28, b'Elgeyo-Marakwet'), (29, b'Nandi'), (30, b'Baringo'), (31, b'Laikipia'), (32, b'Nakuru'), (33, b'Narok'), (34, b'Kajiado'), (35, b'Kericho'), (36, b'Bomet'), (37, b'Kakamega'), (38, b'Vihiga'), (39, b'Bungoma'), (40, b'Busia'), (41, b'Siaya'), (42, b'Kisumu'), (43, b'Homa Bay'), (44, b'Migori'), (45, b'Kisii'), (46, b'Nyamira'), (47, b'Nairobi')]),
        ),
        migrations.AddField(
            model_name='deal',
            name='country',
            field=models.SmallIntegerField(default=2, choices=[(1, b'Nigeria'), (2, b'Kenya')]),
        ),
        migrations.AddField(
            model_name='deal',
            name='location',
            field=models.SmallIntegerField(default=47, choices=[(1, b'Mombasa'), (2, b'Kwale'), (3, b'Kilifi'), (4, b'Tana River'), (5, b'Lamu'), (6, b'Taita-Taveta'), (7, b'Garissa'), (8, b'Wajir'), (9, b'Mandera'), (10, b'Marsabit'), (11, b'Isiolo'), (12, b'Meru'), (13, b'Tharaka-Nithi'), (14, b'Embu'), (15, b'Kitui'), (16, b'Machakos'), (17, b'Makueni'), (18, b'Nyandarua'), (19, b'Nyeri'), (20, b'Kirinyaga'), (21, b"Murang'a"), (22, b'Kiambu'), (23, b'Turkana'), (24, b'West Pokot'), (25, b'Samburu'), (26, b'Trans-Nzoia'), (27, b'Uasin Gishu'), (28, b'Elgeyo-Marakwet'), (29, b'Nandi'), (30, b'Baringo'), (31, b'Laikipia'), (32, b'Nakuru'), (33, b'Narok'), (34, b'Kajiado'), (35, b'Kericho'), (36, b'Bomet'), (37, b'Kakamega'), (38, b'Vihiga'), (39, b'Bungoma'), (40, b'Busia'), (41, b'Siaya'), (42, b'Kisumu'), (43, b'Homa Bay'), (44, b'Migori'), (45, b'Kisii'), (46, b'Nyamira'), (47, b'Nairobi')]),
        ),
        migrations.AlterField(
            model_name='deal',
            name='currency',
            field=models.SmallIntegerField(default=1, choices=[(1, b'N'), (2, b'KES'), (3, b'$')]),
        ),
    ]
