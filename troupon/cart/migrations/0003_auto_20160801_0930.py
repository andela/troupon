# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20160801_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usershippingdetails',
            old_name='userprofile',
            new_name='user',
        ),
    ]
