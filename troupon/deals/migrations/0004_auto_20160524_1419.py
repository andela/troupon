# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0003_auto_20160524_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='location',
            new_name='location_kenya',
        ),
        migrations.AddField(
            model_name='deal',
            name='location_nigeria',
            field=models.SmallIntegerField(default=25, choices=[(1, b'Abia'), (2, b'Abuja FCT'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')]),
        ),
    ]
