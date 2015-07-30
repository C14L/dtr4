# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0016_auto_20150729_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 22, 39, 29, 782652, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 22, 39, 29, 784860, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 22, 39, 29, 789404, tzinfo=utc), db_index=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 22, 39, 29, 789327, tzinfo=utc)),
        ),
    ]
