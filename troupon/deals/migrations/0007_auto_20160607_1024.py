# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_auto_20160531_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='location_kenya',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='location_nigeria',
        ),
        migrations.AddField(
            model_name='deal',
            name='location',
            field=models.SmallIntegerField(default=0, choices=[(38, b'Mombasa'), (39, b'Kwale'), (40, b'Kilifi'), (41, b'Tana River'), (42, b'Lamu'), (43, b'Taita-Taveta'), (44, b'Garissa'), (45, b'Wajir'), (46, b'Mandera'), (47, b'Marsabit'), (48, b'Isiolo'), (49, b'Meru'), (50, b'Tharaka-Nithi'), (51, b'Embu'), (52, b'Kitui'), (53, b'Machakos'), (54, b'Makueni'), (55, b'Nyandarua'), (56, b'Nyeri'), (57, b'Kirinyaga'), (58, b"Murang'a"), (59, b'Kiambu'), (60, b'Turkana'), (61, b'West Pokot'), (62, b'Samburu'), (63, b'Trans-Nzoia'), (64, b'Uasin Gishu'), (65, b'Elgeyo-Marakwet'), (66, b'Nandi'), (67, b'Baringo'), (68, b'Laikipia'), (69, b'Nakuru'), (70, b'Narok'), (71, b'Kajiado'), (72, b'Kericho'), (73, b'Bomet'), (74, b'Kakamega'), (75, b'Vihiga'), (76, b'Bungoma'), (77, b'Busia'), (78, b'Siaya'), (79, b'Kisumu'), (80, b'Homa Bay'), (81, b'Migori'), (82, b'Kisii'), (83, b'Nyamira'), (84, b'Nairobi'), (0, b'None'), (1, b'Abia'), (2, b'Abuja FCT'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')]),
        ),
        migrations.AlterField(
            model_name='advertiser',
            name='location',
            field=models.SmallIntegerField(default=47, choices=[(38, b'Mombasa'), (39, b'Kwale'), (40, b'Kilifi'), (41, b'Tana River'), (42, b'Lamu'), (43, b'Taita-Taveta'), (44, b'Garissa'), (45, b'Wajir'), (46, b'Mandera'), (47, b'Marsabit'), (48, b'Isiolo'), (49, b'Meru'), (50, b'Tharaka-Nithi'), (51, b'Embu'), (52, b'Kitui'), (53, b'Machakos'), (54, b'Makueni'), (55, b'Nyandarua'), (56, b'Nyeri'), (57, b'Kirinyaga'), (58, b"Murang'a"), (59, b'Kiambu'), (60, b'Turkana'), (61, b'West Pokot'), (62, b'Samburu'), (63, b'Trans-Nzoia'), (64, b'Uasin Gishu'), (65, b'Elgeyo-Marakwet'), (66, b'Nandi'), (67, b'Baringo'), (68, b'Laikipia'), (69, b'Nakuru'), (70, b'Narok'), (71, b'Kajiado'), (72, b'Kericho'), (73, b'Bomet'), (74, b'Kakamega'), (75, b'Vihiga'), (76, b'Bungoma'), (77, b'Busia'), (78, b'Siaya'), (79, b'Kisumu'), (80, b'Homa Bay'), (81, b'Migori'), (82, b'Kisii'), (83, b'Nyamira'), (84, b'Nairobi')]),
        ),
    ]
