# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0008_talk_talkhashtag_talkusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='is_blocked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 19, 22, 20, 56, 10862, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
