# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0006_userprofile_active_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermsg',
            name='is_blocked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'man who likes women'), (2, 'man who likes men'), (3, 'man who likes others'), (4, 'woman who likes men'), (5, 'woman who likes women'), (6, 'woman who likes others'), (7, 'other who likes men'), (8, 'other who likes women'), (9, 'other who likes others'), (10, 'asexual'), (11, 'other')], verbose_name='gender', default=0),
            preserve_default=True,
        ),
    ]
