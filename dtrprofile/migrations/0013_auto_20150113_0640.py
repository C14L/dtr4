# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0012_auto_20141225_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lookingfor',
            field=models.SmallIntegerField(default=0, verbose_name='lookingfor', choices=[(0, ''), (1, 'friends only'), (2, 'serious relationship'), (3, 'casual dating'), (4, 'passion'), (5, 'casual sex'), (6, 'not sure yet'), (7, 'marriage')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 6, 40, 53, 119287, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 6, 40, 53, 121224, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2015, 1, 13, 6, 40, 53, 125242, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 6, 40, 53, 125173, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lat',
            field=models.FloatField(db_index=True, default=None, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lng',
            field=models.FloatField(db_index=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
