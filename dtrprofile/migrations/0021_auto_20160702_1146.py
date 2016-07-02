# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0020_auto_20160624_1355'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='userflag',
            index_together=set([('flag_type', 'sender', 'receiver'), ('flag_type', 'receiver', 'sender'), ('sender', 'receiver'), ('receiver', 'sender')]),
        ),
    ]
