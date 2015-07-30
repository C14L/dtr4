# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dtrprofile', '0015_auto_20150120_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='talks', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AlterField(
            model_name='userflag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 16, 50, 13, 938823, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 16, 50, 13, 941060, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutarts',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutbooks',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutfood',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutme',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutmovies',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutmusic',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutquotes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='aboutsports',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='abouttravel',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(blank=True, default=None, to='dtrcity.City', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.ForeignKey(blank=True, default=None, to='dtrcity.Country', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='diet',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'anything'), (2, 'balanced'), (3, 'lots of meat'), (5, 'mostly vegetarian'), (6, 'strictly vegetarian'), (7, 'mostly vegan'), (8, 'strictly vegan'), (9, 'mostly kosher/halal'), (10, 'strictly kosher/halal')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='drink',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'daily'), (2, 'very often'), (3, 'rarely'), (4, 'only socially'), (5, 'mostly never'), (6, 'never-ever')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='eastern_zodiac',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'rat'), (2, 'ox'), (3, 'tiger'), (4, 'rabbit'), (5, 'dragon'), (6, 'snake'), (7, 'horse'), (8, 'goat'), (9, 'monkey'), (10, 'rooster'), (11, 'dog'), (12, 'pig')], default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'some high school'), (2, 'high school graduated'), (3, 'some college'), (4, 'college graduated'), (5, 'some university'), (6, 'university graduate'), (8, 'master program graduate'), (9, 'doctorate'), (7, 'other')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='eyecolor',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'black'), (2, 'blue'), (3, 'brown'), (4, 'green'), (5, 'grey'), (6, 'hazel'), (7, 'other')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='figure',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'mostly bones'), (2, 'slim'), (3, 'average'), (4, 'good curves'), (5, 'overweight'), (6, 'some muscles'), (7, 'only muscles')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fitness',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'muscles'), (2, 'very fit'), (3, 'fit'), (4, 'average'), (5, 'a little lazy'), (6, 'very lazy')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'man who likes women'), (2, 'man who likes men'), (4, 'woman who likes men'), (5, 'woman who likes women'), (11, 'other')], default=11, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='haircolor',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'black'), (2, 'blonde'), (3, 'brown'), (4, 'brunette'), (5, 'red'), (6, 'grey'), (7, 'white'), (8, 'other'), (9, 'bald')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='has_children',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'no'), (2, 'yes, they live with me'), (3, 'yes, but they do not live with me')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.SmallIntegerField(choices=[(0, ''), (134, '< 135 cm / 4\'5"'), (135, '135 cm / 4\'5"'), (136, '136 cm / 4\'6"'), (137, '137 cm / 4\'6"'), (138, '138 cm / 4\'6"'), (139, '139 cm / 4\'7"'), (140, '140 cm / 4\'7"'), (141, '141 cm / 4\'8"'), (142, '142 cm / 4\'8"'), (143, '143 cm / 4\'8"'), (144, '144 cm / 4\'9"'), (145, '145 cm / 4\'9"'), (146, '146 cm / 4\'9"'), (147, '147 cm / 4\'10"'), (148, '148 cm / 4\'10"'), (149, '149 cm / 4\'11"'), (150, '150 cm / 4\'11"'), (151, '151 cm / 4\'11"'), (152, '152 cm / 5\'0"'), (153, '153 cm / 5\'0"'), (154, '154 cm / 5\'1"'), (155, '155 cm / 5\'1"'), (156, '156 cm / 5\'1"'), (157, '157 cm / 5\'2"'), (158, '158 cm / 5\'2"'), (159, '159 cm / 5\'3"'), (160, '160 cm / 5\'3"'), (161, '161 cm / 5\'3"'), (162, '162 cm / 5\'4"'), (163, '163 cm / 5\'4"'), (164, '164 cm / 5\'5"'), (165, '165 cm / 5\'5"'), (166, '166 cm / 5\'5"'), (167, '167 cm / 5\'6"'), (168, '168 cm / 5\'6"'), (169, '169 cm / 5\'7"'), (170, '170 cm / 5\'7"'), (171, '171 cm / 5\'7"'), (172, '172 cm / 5\'8"'), (173, '173 cm / 5\'8"'), (174, '174 cm / 5\'9"'), (175, '175 cm / 5\'9"'), (176, '176 cm / 5\'9"'), (177, '177 cm / 5\'10"'), (178, '178 cm / 5\'10"'), (179, '179 cm / 5\'10"'), (180, '180 cm / 5\'11"'), (181, '181 cm / 5\'11"'), (182, '182 cm / 6\'0"'), (183, '183 cm / 6\'0"'), (184, '184 cm / 6\'0"'), (185, '185 cm / 6\'1"'), (186, '186 cm / 6\'1"'), (187, '187 cm / 6\'2"'), (188, '188 cm / 6\'2"'), (189, '189 cm / 6\'2"'), (190, '190 cm / 6\'3"'), (191, '191 cm / 6\'3"'), (192, '192 cm / 6\'4"'), (193, '193 cm / 6\'4"'), (194, '194 cm / 6\'4"'), (195, '195 cm / 6\'5"'), (196, '196 cm / 6\'5"'), (197, '197 cm / 6\'6"'), (198, '198 cm / 6\'6"'), (199, '199 cm / 6\'6"'), (200, '200 cm / 6\'7"'), (201, '201 cm / 6\'7"'), (202, '202 cm / 6\'8"'), (203, '203 cm / 6\'8"'), (204, '204 cm / 6\'8"'), (205, '205 cm / 6\'9"'), (206, '206 cm / 6\'9"'), (207, '207 cm / 6\'9"'), (208, '208 cm / 6\'10"'), (209, '209 cm / 6\'10"'), (210, '210 cm / 6\'11"'), (211, '> 210 cm / 6\'11"')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='income',
            field=models.SmallIntegerField(choices=[(0, ''), (1, '< $10,000'), (2, '$10,000 - $30,000'), (3, '$30,000 - $60,000'), (5, '$60,000 - $100,000'), (6, '> $100,000')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='jobfield',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'administration'), (2, 'art'), (3, 'banking'), (4, 'construction'), (5, 'education'), (6, 'engineering'), (7, 'entertainment'), (8, 'government'), (9, 'hospitality'), (10, 'internet'), (11, 'law'), (12, 'medicine'), (13, 'marketing'), (14, 'military'), (15, 'finance'), (16, 'management'), (17, 'music'), (18, 'politics'), (20, 'sales'), (21, 'science'), (24, 'technology'), (26, 'transportation'), (28, 'writing'), (90, 'other')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_active',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2015, 7, 29, 16, 50, 13, 945665, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 16, 50, 13, 945585, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longest_relationship',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'never had a serious relationship'), (2, 'only for some months'), (3, 'more than a year'), (4, 'more than three years'), (5, 'more than five years'), (6, 'more than seven years'), (7, 'more than nine years')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lookingfor',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'friends only'), (2, 'serious relationship'), (3, 'casual dating'), (4, 'passion'), (5, 'casual sex'), (6, 'not sure yet'), (7, 'marriage')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='looks',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'gorgeous'), (2, 'very attractive'), (3, 'attractive'), (4, 'average'), (5, 'below average'), (6, 'awfull')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pot',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'daily'), (2, 'very often'), (3, 'rarely'), (4, 'only socially'), (5, 'mostly never'), (6, 'never-ever')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='relationship_status',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'divorced'), (2, 'married'), (3, 'separated'), (4, 'single'), (5, 'widowed'), (6, 'open relationship'), (7, 'poly relationship')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='religion',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'not religious'), (2, 'atheist'), (3, 'agnostic'), (4, 'christian: roman catholic'), (8, 'christian: protestant'), (10, 'christian: other'), (14, 'islam'), (18, 'jewish'), (19, 'bahai'), (22, 'buddhism'), (25, 'hinduism'), (26, 'sikhism'), (27, 'shinto'), (28, 'confucianism'), (29, 'taoism'), (30, 'jainism'), (31, 'zoroastrianism'), (32, 'rastafarian'), (33, 'wicca'), (34, 'spiritualist'), (35, 'indigenous animism'), (36, 'my own religious beliefs'), (37, 'other religious belief')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='religiosity',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'very serious'), (2, 'somewhat serious'), (3, 'not serious'), (9, 'do not care at all')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='smoke',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'heavy smoker'), (2, 'regular smoker'), (3, 'rarely smoke'), (4, 'only socially'), (5, 'trying to quit'), (6, 'non smoker'), (7, 'never-ever')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='spirituality',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'very serious'), (2, 'somewhat serious'), (3, 'not serious'), (9, 'do not care at all')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sports',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'daily doing sports'), (2, 'do sports regularly'), (3, 'sometimes do sports'), (4, 'only watch sports')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='want_children',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'yes, definitely'), (2, 'yes, I think so'), (3, 'not sure'), (4, 'probably not'), (5, 'no, definitely not')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.SmallIntegerField(choices=[(0, ''), (40, '40 kg / 88 lbs'), (41, '41 kg / 90 lbs'), (42, '42 kg / 93 lbs'), (43, '43 kg / 95 lbs'), (44, '44 kg / 97 lbs'), (45, '45 kg / 99 lbs'), (46, '46 kg / 101 lbs'), (47, '47 kg / 104 lbs'), (48, '48 kg / 106 lbs'), (49, '49 kg / 108 lbs'), (50, '50 kg / 110 lbs'), (51, '51 kg / 112 lbs'), (52, '52 kg / 115 lbs'), (53, '53 kg / 117 lbs'), (54, '54 kg / 119 lbs'), (55, '55 kg / 121 lbs'), (56, '56 kg / 123 lbs'), (57, '57 kg / 126 lbs'), (58, '58 kg / 128 lbs'), (59, '59 kg / 130 lbs'), (60, '60 kg / 132 lbs'), (61, '61 kg / 134 lbs'), (62, '62 kg / 137 lbs'), (63, '63 kg / 139 lbs'), (64, '64 kg / 141 lbs'), (65, '65 kg / 143 lbs'), (66, '66 kg / 146 lbs'), (67, '67 kg / 148 lbs'), (68, '68 kg / 150 lbs'), (69, '69 kg / 152 lbs'), (70, '70 kg / 154 lbs'), (71, '71 kg / 157 lbs'), (72, '72 kg / 159 lbs'), (73, '73 kg / 161 lbs'), (74, '74 kg / 163 lbs'), (75, '75 kg / 165 lbs'), (76, '76 kg / 168 lbs'), (77, '77 kg / 170 lbs'), (78, '78 kg / 172 lbs'), (79, '79 kg / 174 lbs'), (80, '80 kg / 176 lbs'), (81, '81 kg / 179 lbs'), (82, '82 kg / 181 lbs'), (83, '83 kg / 183 lbs'), (84, '84 kg / 185 lbs'), (85, '85 kg / 187 lbs'), (86, '86 kg / 190 lbs'), (87, '87 kg / 192 lbs'), (88, '88 kg / 194 lbs'), (89, '89 kg / 196 lbs'), (90, '90 kg / 198 lbs'), (91, '91 kg / 201 lbs'), (92, '92 kg / 203 lbs'), (93, '93 kg / 205 lbs'), (94, '94 kg / 207 lbs'), (95, '95 kg / 209 lbs'), (96, '96 kg / 212 lbs'), (97, '97 kg / 214 lbs'), (98, '98 kg / 216 lbs'), (99, '99 kg / 218 lbs'), (100, '100 kg / 220 lbs'), (101, '101 kg / 223 lbs'), (102, '102 kg / 225 lbs'), (103, '103 kg / 227 lbs'), (104, '104 kg / 229 lbs'), (105, '105 kg / 231 lbs'), (106, '106 kg / 234 lbs'), (107, '107 kg / 236 lbs'), (108, '108 kg / 238 lbs'), (109, '109 kg / 240 lbs'), (110, '110 kg / 243 lbs'), (111, '111 kg / 245 lbs'), (112, '112 kg / 247 lbs'), (113, '113 kg / 249 lbs'), (114, '114 kg / 251 lbs'), (115, '115 kg / 254 lbs'), (116, '116 kg / 256 lbs'), (117, '117 kg / 258 lbs'), (118, '118 kg / 260 lbs'), (119, '119 kg / 262 lbs'), (120, '120 kg / 265 lbs'), (121, '121 kg / 267 lbs'), (122, '122 kg / 269 lbs'), (123, '123 kg / 271 lbs'), (124, '124 kg / 273 lbs'), (125, '125 kg / 276 lbs'), (126, '126 kg / 278 lbs'), (127, '127 kg / 280 lbs'), (128, '128 kg / 282 lbs'), (129, '129 kg / 284 lbs'), (130, '130 kg / 287 lbs')], default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='western_zodiac',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'aries'), (2, 'taurus'), (3, 'gemini'), (4, 'cancer'), (5, 'leo'), (6, 'virgo'), (7, 'libra'), (8, 'scorpio'), (9, 'sagittarius'), (10, 'capricorn'), (11, 'aquarius'), (12, 'pisces')], default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='would_relocate',
            field=models.SmallIntegerField(choices=[(0, ''), (1, 'yes, definitely'), (2, 'not sure'), (3, 'no, definitely not')], default=0),
        ),
    ]
