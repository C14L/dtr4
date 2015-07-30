# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0005_auto_20141209_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_counter',
            field=models.IntegerField(editable=False, default=0),
            preserve_default=True,
        ),
    ]
