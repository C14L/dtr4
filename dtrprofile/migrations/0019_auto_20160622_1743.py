# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0018_auto_20150807_1740'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='userprofile',
            index_together=set([('user', 'city', 'dob', 'gender', 'pic'), ('city', 'dob', 'gender')]),
        ),
    ]
