# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0010_auto_20141220_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 11, 20, 56, 508251, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='flag_type',
            field=models.PositiveIntegerField(choices=[(1, 'friend'), (2, 'like'), (3, 'block'), (4, 'favorite'), (5, 'viewed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 11, 20, 56, 510173, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2014, 12, 21, 11, 20, 56, 514495, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 11, 20, 56, 514424, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
