# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0009_auto_20141219_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='created',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
