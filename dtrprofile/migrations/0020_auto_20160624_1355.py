# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0019_auto_20160622_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='crc',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='language',
        ),
    ]
