# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0002_auto_20141207_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='crc',
            field=models.CharField(editable=False, default='', max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='diet',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'anything'), (2, 'balanced'), (3, 'lots of meat'), (5, 'mostly vegetarian'), (6, 'strictly vegetarian'), (7, 'mostly vegan'), (8, 'strictly vegan'), (9, 'mostly kosher'), (10, 'strictly kosher'), (11, 'mostly halal'), (12, 'strictly halal')], default=0, verbose_name='diet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='drink',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Alcoholic'), (2, 'Regular drinker'), (3, 'Rarely drink'), (4, 'Only socially'), (5, 'Never drink alcohol'), (6, 'Never ever ever!')], default=0, help_text='Do you drink alcohol?', verbose_name='alcohol'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'some High School'), (2, 'high School graduated'), (3, 'some College'), (4, 'college graduated'), (5, 'some University'), (6, 'university graduate'), (8, 'master program graduate'), (9, 'doctorate'), (7, 'other')], default=0, help_text='What is your highest level of education?', verbose_name='education'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='eyecolor',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'black'), (2, 'blue'), (3, 'brown'), (4, 'green'), (5, 'grey'), (6, 'hazel'), (7, 'other')], default=0, help_text='What is your eye color?', verbose_name='eye color'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'man who likes women'), (2, 'man who likes men'), (3, 'man who likes transgender'), (4, 'woman who likes men'), (5, 'woman who likes women'), (6, 'woman who likes transgender'), (7, 'transgender who likes men'), (8, 'transgender who likes women'), (9, 'transgender who likes transgender'), (10, 'man who likes men and women'), (11, 'woman who likes men and women'), (12, 'transgender who likes men and women'), (13, 'asexual'), (14, 'other')], default=0, verbose_name='gender'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='haircolor',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'black'), (2, 'blonde'), (3, 'brown'), (4, 'brunette'), (5, 'red'), (6, 'grey'), (7, 'white'), (8, 'other'), (9, 'bald')], default=0, help_text='What is your hair color?', verbose_name='hair color'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='has_children',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'No'), (2, 'Yes, they live with me'), (3, 'Yes, but they do not live with me')], default=0, help_text='Do you have children?', verbose_name='have children'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='income',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'less than $10,000'), (2, '$10,000 - $30,000'), (3, '$30,000 - $60,000'), (5, '$60,000 - $100,000'), (6, 'more than $100,000')], default=0, help_text='What is you yearly income range?', verbose_name='income range'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='jobfield',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Administration'), (2, 'Art'), (3, 'Banking'), (4, 'Construction'), (5, 'Education'), (6, 'Engineering'), (7, 'Entertainment'), (8, 'Government'), (9, 'Hospitality'), (10, 'Internet'), (11, 'Law'), (12, 'Medicine'), (13, 'Marketing'), (14, 'Military'), (15, 'Finance'), (16, 'Management'), (17, 'Music'), (18, 'Politics'), (20, 'Sales'), (21, 'Science'), (24, 'Technology'), (26, 'Transportation'), (28, 'Writing'), (90, 'Other')], default=0, help_text='What general field do you work in?', verbose_name='occupation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longest_relationship',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Never had a serious relationship'), (2, 'Only some months'), (3, 'More than one year'), (4, 'More than three years'), (5, 'More than five years'), (6, 'More than seven years'), (7, 'More than nine years')], default=0, help_text='How long was your longest relationship?', verbose_name='longest relationship'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pot',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Daily'), (2, 'Very often'), (3, 'Sometimes'), (4, 'Rarely'), (5, 'Mostly never'), (6, 'Never-ever!')], default=0, help_text='Do you smoke marijuana?', verbose_name='marijuana'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='relationship_status',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'divorced'), (2, 'married'), (3, 'separated'), (4, 'single'), (5, 'widowed')], default=0, help_text='What is your relationship status?', verbose_name='relationship status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='religion',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Not religious'), (2, 'Atheist'), (3, 'Agnostic'), (4, 'Christian: Roman Catholic'), (5, 'Christian: Protestant Anglican'), (6, 'Christian: Protestant Lutheran'), (7, 'Christian: Protestant Baptist'), (8, 'Christian: Protestant'), (9, 'Christian: Orthodox'), (10, 'Christian: Other'), (11, 'Islamic: Sunni'), (12, 'Islamic: Shia'), (13, 'Islamic: Sufism'), (14, 'Islamic: Other'), (15, 'Jewish: Orthodox'), (16, 'Jewish: Conservative'), (17, 'Jewish: Reform'), (18, 'Jewish: Other'), (19, "Baha'i"), (20, 'Buddhism: Theravada'), (21, 'Buddhism: Mahayana'), (22, 'Buddhism: Other'), (23, 'Hinduism: Smartism'), (24, 'Hinduism: Vaishnavism'), (25, 'Hinduism: Other'), (26, 'Sikhism'), (27, 'Shinto'), (28, 'Confucianism'), (29, 'Taoism'), (30, 'Jainism'), (31, 'Zoroastrianism'), (32, 'Rastafarian'), (33, 'Neopagan/Wicca/Druidic'), (34, 'Spiritualist'), (35, 'Animism/Indigenous'), (36, 'My own religious beliefs'), (37, 'Other religious belief')], default=0, help_text='What is your religion?', verbose_name='religion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='religiosity',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'very serious'), (2, 'somewhat serious'), (3, 'not serious'), (9, 'Do not care at all')], default=0, help_text='How important is religion to you?', verbose_name='religiosity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='smoke',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Heavy smoker'), (2, 'Regular smoker'), (3, 'Rarely smoke'), (4, 'Only socially'), (5, 'Trying to quit'), (6, 'Non smoker'), (7, 'Never-ever!')], default=0, help_text='Do you smoke tobacco?', verbose_name='tobacco'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='spirituality',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'very serious'), (2, 'somewhat serious'), (3, 'not serious'), (9, 'Do not care at all')], default=0, help_text='How important is spirituality to you?', verbose_name='spirituality'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sports',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'daily doing sports'), (2, 'do sports regularly'), (3, 'sometimes do sports'), (4, 'only watch sports')], default=0, help_text='Do you do any sports?', verbose_name='sports'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='want_children',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Yes, definitely'), (2, 'Yes, I think so'), (3, 'Not sure'), (4, 'Probably not'), (5, 'No, definitely not.')], default=0, help_text='Do you want more children?', verbose_name='want children'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='would_relocate',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'Yes, definitely!'), (2, 'Not sure.'), (3, 'No, never.')], default=0, help_text='If you found someone in a different city, would you move?', verbose_name='would relocate'),
            preserve_default=True,
        ),
    ]
