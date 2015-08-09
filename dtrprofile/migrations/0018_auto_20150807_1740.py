# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0017_auto_20150729_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_email',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='notification_emails',
            field=models.SmallIntegerField(default=0, choices=[(0, 'never'), (1, 'once a months'), (2, 'once a week'), (3, 'once a day'), (4, 'always')]),
        ),
    ]
