# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0003_auto_20141208_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermsg',
            name='created_ip',
            field=models.CharField(default='', blank=True, max_length=15),
            preserve_default=True,
        ),
    ]
