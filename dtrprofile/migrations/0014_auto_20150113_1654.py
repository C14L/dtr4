# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0013_auto_20150113_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 16, 54, 27, 188099, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 16, 54, 27, 190005, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2015, 1, 13, 16, 54, 27, 194485, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 16, 54, 27, 194411, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
