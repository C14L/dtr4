# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dtrprofile', '0007_auto_20141216_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(default=datetime.datetime(2014, 12, 19, 21, 48, 47, 787966, tzinfo=utc))),
                ('created_ip', models.CharField(default='', max_length=15)),
                ('child_counter', models.SmallIntegerField(default=0)),
                ('views_counter', models.SmallIntegerField(default=0)),
                ('hashtag_counter', models.SmallIntegerField(default=0)),
                ('username_counter', models.SmallIntegerField(default=0)),
                ('text', models.TextField()),
                ('parent', models.ForeignKey(default=None, related_name='children', to='dtrprofile.Talk', null=True)),
                ('user', models.ForeignKey(related_name='talks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkHashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tag', models.CharField(db_index=True, max_length=50)),
                ('talk', models.ForeignKey(related_name='hashtag', to='dtrprofile.Talk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkUsername',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('talk', models.ForeignKey(related_name='mentions', to='dtrprofile.Talk')),
                ('user', models.ForeignKey(related_name='mentioned_in', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
