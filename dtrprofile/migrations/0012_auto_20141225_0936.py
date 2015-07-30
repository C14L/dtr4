# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0011_auto_20141221_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 25, 9, 36, 17, 83760, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='receiver',
            field=models.ForeignKey(related_name='was_flagged', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 25, 9, 36, 17, 85747, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(verbose_name='language', default='en', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 25, 9, 36, 17, 90160, tzinfo=utc), db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 25, 9, 36, 17, 90090, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
