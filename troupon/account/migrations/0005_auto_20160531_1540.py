# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160531_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_state',
            new_name='state',
        ),
    ]
