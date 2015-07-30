# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import image_with_thumbnail_field
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('dtrcity', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFlag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('flag_type', models.PositiveIntegerField(choices=[(1, 'friends'), (2, 'like'), (3, 'block')])),
                ('confirmed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserMsg',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('is_read', models.BooleanField(default=False)),
                ('is_replied', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('pic', image_with_thumbnail_field.ImageWithThumbsField(upload_to='raw', default='')),
                ('filesize', models.PositiveIntegerField(default=0)),
                ('width', models.PositiveSmallIntegerField(default=0)),
                ('height', models.PositiveSmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, related_name='profile', to=settings.AUTH_USER_MODEL, editable=False)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('language', models.SmallIntegerField(default=0, verbose_name='language', choices=[('en', 'English'), ('es', 'Español')])),
                ('notification_emails', models.SmallIntegerField(help_text='How often do you want to receive notification emails?', default=0, verbose_name='notification emails', choices=[(0, 'never'), (1, 'once a months'), (2, 'once a week'), (3, 'once a day'), (4, 'always')])),
                ('style_active', models.BooleanField(default=False)),
                ('style', models.TextField(default='', verbose_name='Profile page CSS styles', blank=True)),
                ('friend_open_invites_recv_counter', models.IntegerField(default=0)),
                ('friend_mutual_confirmed_counter', models.IntegerField(default=0)),
                ('match_open_invites_recv_counter', models.IntegerField(default=0)),
                ('match_mutual_confirmed_counter', models.IntegerField(default=0)),
                ('mail_recv_counter', models.IntegerField(default=0)),
                ('mail_sent_counter', models.IntegerField(default=0)),
                ('mail_unread_counter', models.IntegerField(default=0)),
                ('views_counter', models.IntegerField(default=0)),
                ('dob', models.DateField(help_text='Your birth date will be kept private always. Only your age and your zodiac sign will be shown in your profile.', default=None, null=True, verbose_name='birth date', blank=True)),
                ('gender', models.SmallIntegerField(default=0, verbose_name='gender', choices=[(0, ''), (1, 'man who likes women'), (2, 'man who likes men'), (4, 'man who likes transgender'), (8, 'woman who likes men'), (16, 'woman who likes women'), (32, 'woman who likes transgender'), (64, 'transgender who likes men'), (128, 'transgender who likes women'), (256, 'transgender who likes transgender')])),
                ('lat', models.FloatField(db_index=True, default=0.0, blank=True)),
                ('lng', models.FloatField(db_index=True, default=0.0, blank=True)),
                ('aboutme', models.TextField(help_text='Everything about you.', default='', verbose_name='about you', blank=True)),
                ('aboutbooks', models.TextField(help_text='Books you enjoyed and recommend.', default='', verbose_name='favorite books', blank=True)),
                ('aboutmovies', models.TextField(help_text='The best movies you watched.', default='', verbose_name='favorite movies', blank=True)),
                ('aboutmusic', models.TextField(help_text='Music you most enjoy.', default='', verbose_name='favorite music', blank=True)),
                ('aboutarts', models.TextField(help_text='Works of art you like', default='', verbose_name='favorite art works', blank=True)),
                ('abouttravel', models.TextField(help_text='Travel destinations you like to go.', default='', verbose_name='travel destinations', blank=True)),
                ('aboutfood', models.TextField(help_text='Your favorite foods and drinks.', default='', verbose_name='favorite food', blank=True)),
                ('aboutquotes', models.TextField(help_text='The quotations you live by.', default='', verbose_name='favorite quotations', blank=True)),
                ('aboutsports', models.TextField(help_text='Sports you most like to play or watch.', default='', verbose_name='favorite sports', blank=True)),
                ('height', models.SmallIntegerField(default=0, verbose_name='height', choices=[(0, ''), (134, 'Below 135 cm / 4\'5"'), (135, '135 cm / 4\'5"'), (136, '136 cm / 4\'6"'), (137, '137 cm / 4\'6"'), (138, '138 cm / 4\'6"'), (139, '139 cm / 4\'7"'), (140, '140 cm / 4\'7"'), (141, '141 cm / 4\'8"'), (142, '142 cm / 4\'8"'), (143, '143 cm / 4\'8"'), (144, '144 cm / 4\'9"'), (145, '145 cm / 4\'9"'), (146, '146 cm / 4\'9"'), (147, '147 cm / 4\'10"'), (148, '148 cm / 4\'10"'), (149, '149 cm / 4\'11"'), (150, '150 cm / 4\'11"'), (151, '151 cm / 4\'11"'), (152, '152 cm / 5\'0"'), (153, '153 cm / 5\'0"'), (154, '154 cm / 5\'1"'), (155, '155 cm / 5\'1"'), (156, '156 cm / 5\'1"'), (157, '157 cm / 5\'2"'), (158, '158 cm / 5\'2"'), (159, '159 cm / 5\'3"'), (160, '160 cm / 5\'3"'), (161, '161 cm / 5\'3"'), (162, '162 cm / 5\'4"'), (163, '163 cm / 5\'4"'), (164, '164 cm / 5\'5"'), (165, '165 cm / 5\'5"'), (166, '166 cm / 5\'5"'), (167, '167 cm / 5\'6"'), (168, '168 cm / 5\'6"'), (169, '169 cm / 5\'7"'), (170, '170 cm / 5\'7"'), (171, '171 cm / 5\'7"'), (172, '172 cm / 5\'8"'), (173, '173 cm / 5\'8"'), (174, '174 cm / 5\'9"'), (175, '175 cm / 5\'9"'), (176, '176 cm / 5\'9"'), (177, '177 cm / 5\'10"'), (178, '178 cm / 5\'10"'), (179, '179 cm / 5\'10"'), (180, '180 cm / 5\'11"'), (181, '181 cm / 5\'11"'), (182, '182 cm / 6\'0"'), (183, '183 cm / 6\'0"'), (184, '184 cm / 6\'0"'), (185, '185 cm / 6\'1"'), (186, '186 cm / 6\'1"'), (187, '187 cm / 6\'2"'), (188, '188 cm / 6\'2"'), (189, '189 cm / 6\'2"'), (190, '190 cm / 6\'3"'), (191, '191 cm / 6\'3"'), (192, '192 cm / 6\'4"'), (193, '193 cm / 6\'4"'), (194, '194 cm / 6\'4"'), (195, '195 cm / 6\'5"'), (196, '196 cm / 6\'5"'), (197, '197 cm / 6\'6"'), (198, '198 cm / 6\'6"'), (199, '199 cm / 6\'6"'), (200, '200 cm / 6\'7"'), (201, '201 cm / 6\'7"'), (202, '202 cm / 6\'8"'), (203, '203 cm / 6\'8"'), (204, '204 cm / 6\'8"'), (205, '205 cm / 6\'9"'), (206, '206 cm / 6\'9"'), (207, '207 cm / 6\'9"'), (208, '208 cm / 6\'10"'), (209, '209 cm / 6\'10"'), (210, '210 cm / 6\'11"'), (211, 'Over 210 cm / 6\'11"')])),
                ('weight', models.SmallIntegerField(default=0, verbose_name='weight', choices=[(0, ''), (40, '40 kg / 88 lbs'), (41, '41 kg / 90 lbs'), (42, '42 kg / 93 lbs'), (43, '43 kg / 95 lbs'), (44, '44 kg / 97 lbs'), (45, '45 kg / 99 lbs'), (46, '46 kg / 101 lbs'), (47, '47 kg / 104 lbs'), (48, '48 kg / 106 lbs'), (49, '49 kg / 108 lbs'), (50, '50 kg / 110 lbs'), (51, '51 kg / 112 lbs'), (52, '52 kg / 115 lbs'), (53, '53 kg / 117 lbs'), (54, '54 kg / 119 lbs'), (55, '55 kg / 121 lbs'), (56, '56 kg / 123 lbs'), (57, '57 kg / 126 lbs'), (58, '58 kg / 128 lbs'), (59, '59 kg / 130 lbs'), (60, '60 kg / 132 lbs'), (61, '61 kg / 134 lbs'), (62, '62 kg / 137 lbs'), (63, '63 kg / 139 lbs'), (64, '64 kg / 141 lbs'), (65, '65 kg / 143 lbs'), (66, '66 kg / 146 lbs'), (67, '67 kg / 148 lbs'), (68, '68 kg / 150 lbs'), (69, '69 kg / 152 lbs'), (70, '70 kg / 154 lbs'), (71, '71 kg / 157 lbs'), (72, '72 kg / 159 lbs'), (73, '73 kg / 161 lbs'), (74, '74 kg / 163 lbs'), (75, '75 kg / 165 lbs'), (76, '76 kg / 168 lbs'), (77, '77 kg / 170 lbs'), (78, '78 kg / 172 lbs'), (79, '79 kg / 174 lbs'), (80, '80 kg / 176 lbs'), (81, '81 kg / 179 lbs'), (82, '82 kg / 181 lbs'), (83, '83 kg / 183 lbs'), (84, '84 kg / 185 lbs'), (85, '85 kg / 187 lbs'), (86, '86 kg / 190 lbs'), (87, '87 kg / 192 lbs'), (88, '88 kg / 194 lbs'), (89, '89 kg / 196 lbs'), (90, '90 kg / 198 lbs'), (91, '91 kg / 201 lbs'), (92, '92 kg / 203 lbs'), (93, '93 kg / 205 lbs'), (94, '94 kg / 207 lbs'), (95, '95 kg / 209 lbs'), (96, '96 kg / 212 lbs'), (97, '97 kg / 214 lbs'), (98, '98 kg / 216 lbs'), (99, '99 kg / 218 lbs'), (100, '100 kg / 220 lbs'), (101, '101 kg / 223 lbs'), (102, '102 kg / 225 lbs'), (103, '103 kg / 227 lbs'), (104, '104 kg / 229 lbs'), (105, '105 kg / 231 lbs'), (106, '106 kg / 234 lbs'), (107, '107 kg / 236 lbs'), (108, '108 kg / 238 lbs'), (109, '109 kg / 240 lbs'), (110, '110 kg / 243 lbs'), (111, '111 kg / 245 lbs'), (112, '112 kg / 247 lbs'), (113, '113 kg / 249 lbs'), (114, '114 kg / 251 lbs'), (115, '115 kg / 254 lbs'), (116, '116 kg / 256 lbs'), (117, '117 kg / 258 lbs'), (118, '118 kg / 260 lbs'), (119, '119 kg / 262 lbs'), (120, '120 kg / 265 lbs'), (121, '121 kg / 267 lbs'), (122, '122 kg / 269 lbs'), (123, '123 kg / 271 lbs'), (124, '124 kg / 273 lbs'), (125, '125 kg / 276 lbs'), (126, '126 kg / 278 lbs'), (127, '127 kg / 280 lbs'), (128, '128 kg / 282 lbs'), (129, '129 kg / 284 lbs'), (130, '130 kg / 287 lbs')])),
                ('eyecolor', models.SmallIntegerField(help_text='What is your eye color?', default=0, verbose_name='eye color', choices=[(0, ''), (10, 'black'), (20, 'blue'), (30, 'brown'), (40, 'green'), (50, 'grey'), (60, 'hazel'), (70, 'other')])),
                ('haircolor', models.SmallIntegerField(help_text='What is your hair color?', default=0, verbose_name='hair color', choices=[(0, ''), (10, 'black'), (20, 'blonde'), (30, 'brown'), (40, 'brunette'), (50, 'red'), (60, 'grey'), (70, 'white'), (80, 'other'), (90, 'bald')])),
                ('relationship_status', models.SmallIntegerField(help_text='What is your relationship status?', default=0, verbose_name='relationship status', choices=[(0, ''), (10, 'divorced'), (20, 'married'), (30, 'separated'), (40, 'single'), (50, 'widowed')])),
                ('has_children', models.SmallIntegerField(help_text='Do you have children?', default=0, verbose_name='have children', choices=[(0, ''), (10, 'No'), (20, 'Yes, they live with me'), (30, 'Yes, but they do not live with me')])),
                ('want_children', models.SmallIntegerField(help_text='Do you want more children?', default=0, verbose_name='want children', choices=[(0, ''), (10, 'Yes, definitely'), (20, 'Yes, I think so'), (30, 'Not sure'), (40, 'Probably not'), (50, 'No, definitely not.')])),
                ('would_relocate', models.SmallIntegerField(help_text='If you found someone in a different city, would you move?', default=0, verbose_name='would relocate', choices=[(0, ''), (10, 'Yes, definitely!'), (20, 'Not sure.'), (30, 'No, never.')])),
                ('smoke', models.SmallIntegerField(help_text='Do you smoke tobacco?', default=0, verbose_name='tobacco', choices=[(0, ''), (10, 'Heavy smoker'), (20, 'Regular smoker'), (50, 'Trying to quit'), (30, 'Rarely smoke'), (40, 'Only socially'), (60, 'Non smoker'), (70, 'Never-ever!')])),
                ('pot', models.SmallIntegerField(help_text='Do you smoke marijuana?', default=0, verbose_name='marijuana', choices=[(0, ''), (10, 'Daily'), (50, 'Very often'), (20, 'Regularly'), (30, 'Sometimes'), (40, 'Rarely'), (60, 'Mostly never'), (70, 'Never-ever!')])),
                ('drink', models.SmallIntegerField(help_text='Do you drink alcohol?', default=0, verbose_name='alcohol', choices=[(0, ''), (10, 'Alcoholic'), (20, 'Regular drinker'), (30, 'Rarely drink'), (40, 'Only socially'), (50, 'Never drink alcohol'), (70, 'Never ever ever!')])),
                ('longest_relationship', models.SmallIntegerField(help_text='How long was your longest relationship?', default=0, verbose_name='longest relationship', choices=[(0, ''), (10, 'Never had a serious relationship'), (15, 'Only some months'), (20, 'More than one year'), (30, 'More than three years'), (40, 'More than five years'), (50, 'More than seven years'), (60, 'More than nine years')])),
                ('education', models.SmallIntegerField(help_text='What is your highest level of education?', default=0, verbose_name='education', choices=[(0, ''), (10, 'some High School'), (20, 'high School graduated'), (30, 'some College'), (40, 'college graduated'), (50, 'some University'), (60, 'university graduate'), (63, 'master program graduate'), (66, 'doctorate'), (70, 'other')])),
                ('diet', models.SmallIntegerField(default=0, verbose_name='diet', choices=[(0, ''), (10, 'anything'), (20, 'balanced'), (30, 'lots of meat'), (50, 'mostly vegetarian'), (60, 'strictly vegetarian'), (70, 'mostly vegan'), (80, 'strictly vegan'), (90, 'mostly kosher'), (100, 'strictly kosher'), (110, 'mostly halal'), (120, 'strictly halal')])),
                ('sports', models.SmallIntegerField(help_text='Do you do any sports?', default=0, verbose_name='sports', choices=[(0, ''), (10, 'daily doing sports'), (20, 'do sports regularly'), (30, 'sometimes do sports'), (40, 'only watch sports')])),
                ('religion', models.SmallIntegerField(help_text='What is your religion?', default=0, verbose_name='religion', choices=[(0, ''), (10, 'Not religious'), (20, 'Atheist'), (30, 'Agnostic'), (40, 'Christian: Roman Catholic'), (50, 'Christian: Protestant Anglican'), (60, 'Christian: Protestant Lutheran'), (70, 'Christian: Protestant Baptist'), (80, 'Christian: Protestant'), (90, 'Christian: Orthodox'), (100, 'Christian: Other'), (110, 'Islamic: Sunni'), (120, 'Islamic: Shia'), (130, 'Islamic: Sufism'), (140, 'Islamic: Other'), (150, 'Jewish: Orthodox'), (160, 'Jewish: Conservative'), (170, 'Jewish: Reform'), (180, 'Jewish: Other'), (190, "Baha'i"), (200, 'Buddhism: Theravada'), (210, 'Buddhism: Mahayana'), (220, 'Buddhism: Other'), (230, 'Hinduism: Smartism'), (240, 'Hinduism: Vaishnavism'), (250, 'Hinduism: Other'), (260, 'Sikhism'), (270, 'Shinto'), (280, 'Confucianism'), (290, 'Taoism'), (300, 'Jainism'), (310, 'Zoroastrianism'), (320, 'Rastafarian'), (330, 'Neopagan/Wicca/Druidic'), (340, 'Spiritualist'), (350, 'Animism/Indigenous'), (360, 'My own religious beliefs'), (370, 'Other religious belief')])),
                ('religiosity', models.SmallIntegerField(help_text='How important is religion to you?', default=0, verbose_name='religiosity', choices=[(0, ''), (10, 'very serious'), (20, 'somewhat serious'), (30, 'not serious'), (90, 'Do not care at all')])),
                ('spirituality', models.SmallIntegerField(help_text='How important is spirituality to you?', default=0, verbose_name='spirituality', choices=[(0, ''), (10, 'very serious'), (20, 'somewhat serious'), (30, 'not serious'), (90, 'Do not care at all')])),
                ('jobfield', models.SmallIntegerField(help_text='What general field do you work in?', default=0, verbose_name='occupation', choices=[(0, ''), (10, 'Administration'), (20, 'Art'), (30, 'Banking'), (40, 'Construction'), (50, 'Education'), (60, 'Engineering'), (70, 'Entertainment'), (80, 'Government'), (90, 'Hospitality'), (100, 'Internet'), (110, 'Law'), (120, 'Medicine'), (130, 'Marketing'), (140, 'Military'), (150, 'Finance'), (160, 'Management'), (170, 'Music'), (180, 'Politics'), (200, 'Sales'), (210, 'Science'), (240, 'Technology'), (260, 'Transportation'), (280, 'Writing'), (900, 'Other')])),
                ('income', models.SmallIntegerField(help_text='What is you yearly income range?', default=0, verbose_name='income range', choices=[(0, ''), (10, 'less than $10,000'), (20, '$10,000 - $30,000'), (30, '$30,000 - $60,000'), (50, '$60,000 - $100,000'), (60, 'more than $100,000')])),
                ('western_zodiac', models.SmallIntegerField(default=0, verbose_name='western zodiac', editable=False, choices=[(0, ''), (1, 'Aries'), (2, 'Taurus'), (3, 'Gemini'), (4, 'Cancer'), (5, 'Leo'), (6, 'Virgo'), (7, 'Libra'), (8, 'Scorpio'), (9, 'Sagittarius'), (10, 'Capricorn'), (11, 'Aquarius'), (12, 'Pisces')])),
                ('eastern_zodiac', models.SmallIntegerField(default=0, verbose_name='eastern zodiac', editable=False, choices=[(0, ''), (1, 'Rat'), (2, 'Ox'), (3, 'Tiger'), (4, 'Rabbit'), (5, 'Dragon'), (6, 'Snake'), (7, 'Horse'), (8, 'Goat'), (9, 'Monkey'), (10, 'Rooster'), (11, 'Dog'), (12, 'Pig')])),
                ('city', models.ForeignKey(default=None, blank=True, verbose_name='city', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dtrcity.City')),
                ('country', models.ForeignKey(default=None, blank=True, verbose_name='country', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dtrcity.Country')),
                ('pic', models.ForeignKey(default=None, blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dtrprofile.UserPic', editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userpic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermsg',
            name='from_user',
            field=models.ForeignKey(related_name='from', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usermsg',
            name='to_user',
            field=models.ForeignKey(related_name='to', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='usermsg',
            index_together=set([('from_user', 'to_user'), ('to_user', 'from_user')]),
        ),
        migrations.AddField(
            model_name='userflag',
            name='receiver',
            field=models.ForeignKey(related_name='was_fagged', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userflag',
            name='sender',
            field=models.ForeignKey(related_name='has_flagged', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='userflag',
            unique_together=set([('sender', 'receiver', 'flag_type')]),
        ),
        migrations.AlterIndexTogether(
            name='userflag',
            index_together=set([('sender', 'receiver')]),
        ),
    ]
