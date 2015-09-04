# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20150903_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='account',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='password',
        ),
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AddField(
            model_name='account',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=django.utils.timezone.now, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
