# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160524_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_country',
            new_name='user_state',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_location',
        ),
    ]
