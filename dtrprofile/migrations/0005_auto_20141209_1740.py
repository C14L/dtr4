# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0004_usermsg_created_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userflag',
            name='confirmed',
            field=models.DateTimeField(default=None, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usermsg',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, related_name='msg_sent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usermsg',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, related_name='msg_received'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='pics'),
            preserve_default=True,
        ),
    ]
