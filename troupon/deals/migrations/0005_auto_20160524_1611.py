# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0004_auto_20160524_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiser',
            name='location',
            field=models.SmallIntegerField(default=47, choices=[(0, b'None'), (1, b'Mombasa'), (2, b'Kwale'), (3, b'Kilifi'), (4, b'Tana River'), (5, b'Lamu'), (6, b'Taita-Taveta'), (7, b'Garissa'), (8, b'Wajir'), (9, b'Mandera'), (10, b'Marsabit'), (11, b'Isiolo'), (12, b'Meru'), (13, b'Tharaka-Nithi'), (14, b'Embu'), (15, b'Kitui'), (16, b'Machakos'), (17, b'Makueni'), (18, b'Nyandarua'), (19, b'Nyeri'), (20, b'Kirinyaga'), (21, b"Murang'a"), (22, b'Kiambu'), (23, b'Turkana'), (24, b'West Pokot'), (25, b'Samburu'), (26, b'Trans-Nzoia'), (27, b'Uasin Gishu'), (28, b'Elgeyo-Marakwet'), (29, b'Nandi'), (30, b'Baringo'), (31, b'Laikipia'), (32, b'Nakuru'), (33, b'Narok'), (34, b'Kajiado'), (35, b'Kericho'), (36, b'Bomet'), (37, b'Kakamega'), (38, b'Vihiga'), (39, b'Bungoma'), (40, b'Busia'), (41, b'Siaya'), (42, b'Kisumu'), (43, b'Homa Bay'), (44, b'Migori'), (45, b'Kisii'), (46, b'Nyamira'), (47, b'Nairobi')]),
        ),
        migrations.AlterField(
            model_name='deal',
            name='location_kenya',
            field=models.SmallIntegerField(default=0, choices=[(0, b'None'), (1, b'Mombasa'), (2, b'Kwale'), (3, b'Kilifi'), (4, b'Tana River'), (5, b'Lamu'), (6, b'Taita-Taveta'), (7, b'Garissa'), (8, b'Wajir'), (9, b'Mandera'), (10, b'Marsabit'), (11, b'Isiolo'), (12, b'Meru'), (13, b'Tharaka-Nithi'), (14, b'Embu'), (15, b'Kitui'), (16, b'Machakos'), (17, b'Makueni'), (18, b'Nyandarua'), (19, b'Nyeri'), (20, b'Kirinyaga'), (21, b"Murang'a"), (22, b'Kiambu'), (23, b'Turkana'), (24, b'West Pokot'), (25, b'Samburu'), (26, b'Trans-Nzoia'), (27, b'Uasin Gishu'), (28, b'Elgeyo-Marakwet'), (29, b'Nandi'), (30, b'Baringo'), (31, b'Laikipia'), (32, b'Nakuru'), (33, b'Narok'), (34, b'Kajiado'), (35, b'Kericho'), (36, b'Bomet'), (37, b'Kakamega'), (38, b'Vihiga'), (39, b'Bungoma'), (40, b'Busia'), (41, b'Siaya'), (42, b'Kisumu'), (43, b'Homa Bay'), (44, b'Migori'), (45, b'Kisii'), (46, b'Nyamira'), (47, b'Nairobi')]),
        ),
        migrations.AlterField(
            model_name='deal',
            name='location_nigeria',
            field=models.SmallIntegerField(default=0, choices=[(0, b'None'), (1, b'Abia'), (2, b'Abuja FCT'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')]),
        ),
    ]
