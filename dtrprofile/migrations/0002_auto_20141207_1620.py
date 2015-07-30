# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpic',
            name='filesize',
        ),
        migrations.RemoveField(
            model_name='userpic',
            name='height',
        ),
        migrations.RemoveField(
            model_name='userpic',
            name='width',
        ),
        migrations.AddField(
            model_name='userpic',
            name='created_ip',
            field=models.CharField(max_length=15, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='flag_type',
            field=models.PositiveIntegerField(choices=[(1, 'friend'), (2, 'like'), (3, 'block'), (4, 'favorite')]),
            preserve_default=True,
        ),
    ]
