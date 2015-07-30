# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0014_auto_20150113_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='figure',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'only bones'), (2, 'slim'), (3, 'average'), (4, 'good curves'), (5, 'overweight'), (6, 'some muscles'), (7, 'muscles only')], help_text='How is your figure?', verbose_name='figure', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fitness',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'all muscles'), (2, 'very fit'), (3, 'fit'), (4, 'average'), (5, 'a little lazy'), (6, 'very lazy')], help_text='How is your fitness?', verbose_name='fitness', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='looks',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'gorgeous'), (2, 'very attractive'), (3, 'attractive'), (4, 'average'), (5, 'below average'), (6, 'awfull')], help_text='How are your looks?', verbose_name='looks', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 8, 37, 41, 983539, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 8, 37, 41, 985435, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='diet',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'anything'), (2, 'balanced'), (3, 'lots of meat'), (5, 'mostly vegetarian'), (6, 'strictly vegetarian'), (7, 'mostly vegan'), (8, 'strictly vegan'), (9, 'mostly kosher'), (10, 'strictly kosher'), (11, 'mostly halal'), (12, 'strictly halal')], help_text='What is your preferred diet?', verbose_name='diet', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 8, 37, 41, 989882, tzinfo=utc), db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 8, 37, 41, 989810, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
