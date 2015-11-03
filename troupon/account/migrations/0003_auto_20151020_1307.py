# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151014_1615'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
