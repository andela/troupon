# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160531_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='state',
            new_name='country',
        ),
    ]
