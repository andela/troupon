# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=1000)),
                ('rating', models.SmallIntegerField(default=5, choices=[(1, b'1 star'), (2, b'2 star'), (3, b'3 star'), (4, b'4 star'), (5, b'5 star')])),
                ('date_created', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('deal', models.ForeignKey(to='deals.Deal')),
            ],
        ),
    ]
