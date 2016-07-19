# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('type', models.SmallIntegerField(default=1, choices=[(1, b'Account'), (2, b'Billing'), (3, b'General Info & Getting Started'), (4, b'Marketplace')])),
                ('sent_at', models.DateTimeField(null=True, blank=True)),
                ('read_at', models.DateTimeField(null=True, blank=True)),
                ('replied_at', models.DateTimeField(null=True, blank=True)),
                ('sender_deleted_at', models.DateTimeField(null=True, blank=True)),
                ('recipient_deleted_at', models.DateTimeField(null=True, blank=True)),
                ('parent_msg', models.ForeignKey(related_name='parent_rel', blank=True, to='conversations.Message', null=True)),
                ('recipient', models.ForeignKey(related_name='recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sender', models.ForeignKey(related_name='sender', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
