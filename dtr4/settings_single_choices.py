# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals, absolute_import, division, print_function
)

from django.utils.translation import ugettext_lazy as _  # ugettext

"""Make Javascript files, one for each language, with the translations
of these choice fields. For example:

- /static/tr-choices-de.js
- /static/tr-choices-en.js

window.TR_CHOICES = {'NOTIFICATION_EMAILS': [[0,'never'], [1,'once a months'],
                     ... [4,'always'] ], ...}
"""

JS_TRANSLATIONS_CHOICES = (
    'NOTIFICATION_EMAILS', 'LOOKINGFOR_CHOICE',
    'GENDER_CHOICE', 'GENDER_PLURAL_CHOICE', 'GENDER_SHORT',
    'GENDER_CHOICE_SYMBOL', 'GENDER_CHOICE_HESHE', 'GENDER_CHOICE_HISHER',
    'EYECOLOR_CHOICE', 'HAIRCOLOR_CHOICE', 'RELATIONSHIP_STATUS_CHOICE',
    'HAS_CHILDREN_CHOICE', 'WANT_CHILDREN_CHOICE', 'WOULD_RELOCATE_CHOICE',
    'SMOKE_CHOICE', 'POT_CHOICE', 'DRINK_CHOICE', 'LONGEST_RELATIONSHIP_CHOICE',
    'LOOKS_CHOICE', 'FIGURE_CHOICE', 'FITNESS_CHOICE', 'SPORTS_CHOICE',
    'RELIGION_CHOICE', 'RELIGIOSITY_CHOICE', 'SPIRITUALITY_CHOICE',
    'EDUCATION_CHOICE', 'WESTERN_ZODIAC_CHOICE', 'WESTERN_ZODIAC_SYMBOLS',
    'EASTERN_ZODIAC_CHOICE', 'EASTERN_ZODIAC_SYMBOLS', 'HEIGHT_CHOICE',
    'WEIGHT_CHOICE', 'DIET_CHOICE', 'JOBFIELD_CHOICE', 'INCOME_CHOICE',
)

# ------------------------------------------------------------------------------

NOTIFICATION_EMAILS = (
    (0, 'never'),
    (1, 'once a months'),
    (2, 'once a week'),
    (3, 'once a day'),
    (4, 'always'),  # whenever sth. happens (recv.message, friend req., etc)
)

LOOKINGFOR_CHOICE = (
    (0, ''),
    (1, _('friends only')),  # Solo amigos
    (2, _('serious relationship')),  # Amor verdadero
    (3, _('casual dating')),  # Un Free
    (4, _('passion')),  # Pasión
    (5, _('casual sex')),  # Una noche y ya!
    (6, _('not sure yet')),  # Lo que se dé
    (7, _('marriage')),  # Matrimonio
)

GENDER_CHOICE = (
    # (0, ''),
    (1, _('man who likes women')),
    (2, _('man who likes men')),
    # (3, _('man who likes others')),
    (4, _('woman who likes men')),
    (5, _('woman who likes women')),
    # (6, _('woman who likes others')),
    # (7, _('other who likes men')),
    # (8, _('other who likes women')),
    # (9, _('other who likes others')),
    # (10, _('asexual')),
    (11, _('other')),
)

GENDER_PLURAL_CHOICE = (
    # (0, ''),
    (1, _('men who like women')),
    (2, _('men who like men')),
    # (3, _('men who like others')),
    (4, _('women who like men')),
    (5, _('women who like women')),
    # (6, _('women who like others')),
    # (7, _('others who like men')),
    # (8, _('others who like women')),
    # (9, _('others who like others')),
    # (10, _('asexuals')),
    (11, _('others')),
)

GENDER_SHORT = (
    # (0, ''),
    (1, _('man')),
    (2, _('man')),
    # (3, _('man')),
    (4, _('woman')),
    (5, _('woman')),
    # (6, _('woman')),
    # (7, _('other')),
    # (8, _('other')),
    # (9, _('other')),
    # (10, _('asexual')),
    (11, _('other')),
)

GENDER_CHOICE_SYMBOL = (
    # (0, ''),
    (1, '♂'),
    (2, '♂'),
    # (3, '♂'),
    (4, '♀'),
    (5, '♀'),
    # (6, '♀'),
    # (7, '⚥'),
    # (8, '⚥'),
    # (9, '⚥'),
    # (10, 'o'),
    (11, '⚥'),
)

GENDER_CHOICE_HESHE = (
    # (0, ''),
    (1, _('he')),
    (2, _('he')),
    # (3, _('he')),
    (4, _('she')),
    (5, _('she')),
    # (6, _('she')),
    # (7, _('they')),
    # (8, _('they')),
    # (9, _('they')),
    # (10, _('they')),
    (11, _('they')),
)

GENDER_CHOICE_HISHER = (
    # (0, ''),
    (1, _('his')),
    (2, _('his')),
    # (3, _('his')),
    (4, _('her')),
    (5, _('her')),
    # (6, _('her')),
    # (7, _('their')),
    # (8, _('their')),
    # (9, _('their')),
    # (10, _('their')),
    (11, _('their')),
)

EYECOLOR_CHOICE = (
    (0, ''),
    (1, _('black')),
    (2, _('blue')),
    (3, _('brown')),
    (4, _('green')),
    (5, _('grey')),
    (6, _('hazel')),
    (7, _('other')),
)

HAIRCOLOR_CHOICE = (
    (0, ''),
    (1, _('black')),
    (2, _('blonde')),
    (3, _('brown')),
    (4, _('brunette')),
    (5, _('red')),
    (6, _('grey')),
    (7, _('white')),
    (8, _('other')),
    (9, _('bald')),
)

RELATIONSHIP_STATUS_CHOICE = (
    (0, ''),
    (1, _('divorced')),
    (2, _('married')),
    (3, _('separated')),
    (4, _('single')),
    (5, _('widowed')),
    (6, _('open relationship')),
    (7, _('poly relationship')),
)

HAS_CHILDREN_CHOICE = (
    (0, ''),
    (1, _('no')),
    (2, _('yes, they live with me')),
    (3, _('yes, but they do not live with me')),
)

WANT_CHILDREN_CHOICE = (
    (0, ''),
    (1, _('yes, definitely')),
    (2, _('yes, I think so')),
    (3, _('not sure')),
    (4, _('probably not')),
    (5, _('no, definitely not')),
)

WOULD_RELOCATE_CHOICE = (
    (0, ''),
    (1, _('yes, definitely')),
    (2, _('not sure')),
    (3, _('no, definitely not')),
)

SMOKE_CHOICE = (
    (0, ''),
    (1, _('heavy smoker')),
    (2, _('regular smoker')),
    (3, _('rarely smoke')),
    (4, _('only socially')),
    (5, _('trying to quit')),
    (6, _('non smoker')),
    (7, _('never-ever')),
)

POT_CHOICE = (
    (0, ''),
    (1, _('daily')),
    (2, _('very often')),
    (3, _('rarely')),
    (4, _('only socially')),
    (5, _('mostly never')),
    (6, _('never-ever')),
)

DRINK_CHOICE = (
    (0, ''),
    (1, _('daily')),
    (2, _('very often')),
    (3, _('rarely')),
    (4, _('only socially')),
    (5, _('mostly never')),
    (6, _('never-ever')),
)

LONGEST_RELATIONSHIP_CHOICE = (
    (0, ''),
    (1, _('never had a serious relationship')),
    (2, _('only for some months')),
    (3, _('more than a year')),
    (4, _('more than three years')),
    (5, _('more than five years')),
    (6, _('more than seven years')),
    (7, _('more than nine years')),
)

LOOKS_CHOICE = (
    (0, ''),
    (1, _('gorgeous')),
    (2, _('very attractive')),
    (3, _('attractive')),
    (4, _('average')),
    (5, _('below average')),
    (6, _('awfull')),
)

FIGURE_CHOICE = (
    (0, ''),
    (1, _('mostly bones')),
    (2, _('slim')),
    (3, _('average')),
    (4, _('good curves')),
    (5, _('overweight')),
    (6, _('some muscles')),
    (7, _('only muscles')),
)

FITNESS_CHOICE = (
    (0, ''),
    (1, _('muscles')),
    (2, _('very fit')),
    (3, _('fit')),
    (4, _('average')),
    (5, _('a little lazy')),
    (6, _('very lazy')),
)

SPORTS_CHOICE = (
    (0, ''),
    (1, _('daily doing sports')),
    (2, _('do sports regularly')),
    (3, _('sometimes do sports')),
    (4, _('only watch sports')),
)

RELIGION_CHOICE = (
    (0, ''),
    (1, _('not religious')),
    (2, _('atheist')),
    (3, _('agnostic')),
    (4, _('christian: roman catholic')),
    # ( 5, _('Christian: Protestant Anglican')),
    # ( 6, _('Christian: Protestant Lutheran')),
    # ( 7, _('Christian: Protestant Baptist')),
    (8, _('christian: protestant')),
    # ( 9, _('Christian: Orthodox')),
    (10, _('christian: other')),
    # (11, _('Islam: Sunni')),
    # (12, _('Islam: Shia')),
    # (13, _('Islam: Sufism')),
    (14, _('islam')),
    # (15, _('Jewish: Orthodox')),
    # (16, _('Jewish: Conservative')),
    # (17, _('Jewish: Reform')),
    (18, _('jewish')),
    (19, _('bahai')),
    # (20, _('Buddhism: Theravada')),
    # (21, _('Buddhism: Mahayana')),
    (22, _('buddhism')),
    # (23, _('Hinduism: Smartism')),
    # (24, _('Hinduism: Vaishnavism')),
    (25, _('hinduism')),
    (26, _('sikhism')),
    (27, _('shinto')),
    (28, _('confucianism')),
    (29, _('taoism')),
    (30, _('jainism')),
    (31, _('zoroastrianism')),
    (32, _('rastafarian')),
    (33, _('wicca')),
    (34, _('spiritualist')),
    (35, _('indigenous animism')),
    (36, _('my own religious beliefs')),
    (37, _('other religious belief')),
)

RELIGIOSITY_CHOICE = (
    (0, ''),
    (1, _('very serious')),
    (2, _('somewhat serious')),
    (3, _('not serious')),
    (9, _('do not care at all')),
)

SPIRITUALITY_CHOICE = (
    (0, ''),
    (1, _('very serious')),
    (2, _('somewhat serious')),
    (3, _('not serious')),
    (9, _('do not care at all')),
)

EDUCATION_CHOICE = (
    (0, ''),
    (1, _('some high school')),
    (2, _('high school graduated')),
    (3, _('some college')),
    (4, _('college graduated')),
    (5, _('some university')),
    (6, _('university graduate')),
    (8, _('master program graduate')),
    (9, _('doctorate')),
    (7, _('other')),
)

WESTERN_ZODIAC_CHOICE = (
    (0, ''),
    (1, _('aries')),
    (2, _('taurus')),
    (3, _('gemini')),
    (4, _('cancer')),
    (5, _('leo')),
    (6, _('virgo')),
    (7, _('libra')),
    (8, _('scorpio')),
    (9, _('sagittarius')),
    (10, _('capricorn')),
    (11, _('aquarius')),
    (12, _('pisces')),
)

WESTERN_ZODIAC_SYMBOLS = (
    (1, '♈'), (2, '♉'), (3, '♊'), (4,  '♋'), (5,  '♌'), (6,  '♍'),
    (7, '♎'), (8, '♏'), (9, '♐'), (10, '♑'), (11, '♒'), (12, '♓'),
)

WESTERN_ZODIAC_UPPER_LIMIT = (
    (120, 10), (218, 11), (320, 12), (420, 1), (521, 2), (621, 3), (722, 4),
    (823, 5), (923, 6), (1023, 7), (1122, 8), (1222, 9), (1231, 10),
)

EASTERN_ZODIAC_CHOICE = (
    (0, ''),
    (1, _('rat')),
    (2, _('ox')),
    (3, _('tiger')),
    (4, _('rabbit')),
    (5, _('dragon')),
    (6, _('snake')),
    (7, _('horse')),
    (8, _('goat')),
    (9, _('monkey')),
    (10, _('rooster')),
    (11, _('dog')),
    (12, _('pig')),
)

EASTERN_ZODIAC_SYMBOLS = (
    (1, '鼠'), (2, '牛'), (3, '虎'), (4, '兔'), (5, '龍'), (6, '蛇'),
    (7, '馬'), (8, '羊'), (9, '猴'), (10, '鷄'), (11, '狗'), (12, '猪'),
)

EASTERN_ZODIAC_UPPER_LIMIT = (
    (19250123, 1), (19260212,  2), (19270201,  3), (19280122,  4),
    (19290209, 5), (19300129,  6), (19310216,  7), (19320205,  8),
    (19330125, 9), (19340213, 10), (19350203, 11), (19360123, 12),
    (19370210, 1), (19380130,  2), (19390218,  3), (19400207,  4),
    (19410126, 5), (19420214,  6), (19430204,  7), (19440124,  8),
    (19450212, 9), (19460201, 10), (19470127, 11), (19480209, 12),
    (19490128, 1), (19500216,  2), (19510205,  3), (19520126,  4),
    (19530213, 5), (19540202,  6), (19550123,  7), (19560211,  8),
    (19570130, 9), (19580217, 10), (19590207, 11), (19600127, 12),
    (19610214, 1), (19620204,  2), (19630124,  3), (19640212,  4),
    (19650201, 5), (19660120,  6), (19670208,  7), (19680129,  8),
    (19690216, 9), (19700205, 10), (19710126, 11), (19720214, 12),
    (19730202, 1), (19740122,  2), (19750210,  3), (19760130,  4),
    (19770217, 5), (19780206,  6), (19790127,  7), (19800215,  8),
    (19810204, 9), (19820124, 10), (19830212, 11), (19840201, 12),
    (19850219, 1), (19860208,  2), (19870128,  3), (19880216,  4),
    (19890205, 5), (19900126,  6), (19910214,  7), (19920203,  8),
    (19930122, 9), (19940209, 10), (19950130, 11), (19960218, 12),
    (19970206, 1), (19980127,  2), (19990215,  3), (20000204,  4),
    (20010123, 5), (20020211,  6), (20030131,  7), (20040121,  8),
    (20050208, 9), (20060128, 10), (20070217, 11), (20080206, 12),
    (20090125, 1), (20100213,  2), (20110202,  3), (20120122,  4),
    (20130209, 5), (20140130,  6), (20150218,  7), (20160207,  8),
    (20170127, 9), (20180215, 10), (20190204, 11), (20200124, 12),
    (20210211, 1), (20220131,  2), (20230121,  3), (20240209,  4),
    (20250128, 5), (20260216,  6), (20270205,  7), (20280125,  8),
    (20290212, 9), (20300202, 10), (20310122, 11), (20320210, 12),
    (20330130, 1), (20340218,  2), (20350207,  3), (20360127,  4),
    (20370214, 5), (20380203,  6), (20390123,  7), (20400211,  8),
    (20410131, 9), (20420121, 10), (20430209, 11), (20440129, 12),
)

HEIGHT_CHOICE = (
    (0, ''),
    (134, "< 135 cm / 4'5\""),
    (135, "135 cm / 4'5\""),
    (136, "136 cm / 4'6\""),
    (137, "137 cm / 4'6\""),
    (138, "138 cm / 4'6\""),
    (139, "139 cm / 4'7\""),
    (140, "140 cm / 4'7\""),
    (141, "141 cm / 4'8\""),
    (142, "142 cm / 4'8\""),
    (143, "143 cm / 4'8\""),
    (144, "144 cm / 4'9\""),
    (145, "145 cm / 4'9\""),
    (146, "146 cm / 4'9\""),
    (147, "147 cm / 4'10\""),
    (148, "148 cm / 4'10\""),
    (149, "149 cm / 4'11\""),
    (150, "150 cm / 4'11\""),
    (151, "151 cm / 4'11\""),
    (152, "152 cm / 5'0\""),
    (153, "153 cm / 5'0\""),
    (154, "154 cm / 5'1\""),
    (155, "155 cm / 5'1\""),
    (156, "156 cm / 5'1\""),
    (157, "157 cm / 5'2\""),
    (158, "158 cm / 5'2\""),
    (159, "159 cm / 5'3\""),
    (160, "160 cm / 5'3\""),
    (161, "161 cm / 5'3\""),
    (162, "162 cm / 5'4\""),
    (163, "163 cm / 5'4\""),
    (164, "164 cm / 5'5\""),
    (165, "165 cm / 5'5\""),
    (166, "166 cm / 5'5\""),
    (167, "167 cm / 5'6\""),
    (168, "168 cm / 5'6\""),
    (169, "169 cm / 5'7\""),
    (170, "170 cm / 5'7\""),
    (171, "171 cm / 5'7\""),
    (172, "172 cm / 5'8\""),
    (173, "173 cm / 5'8\""),
    (174, "174 cm / 5'9\""),
    (175, "175 cm / 5'9\""),
    (176, "176 cm / 5'9\""),
    (177, "177 cm / 5'10\""),
    (178, "178 cm / 5'10\""),
    (179, "179 cm / 5'10\""),
    (180, "180 cm / 5'11\""),
    (181, "181 cm / 5'11\""),
    (182, "182 cm / 6'0\""),
    (183, "183 cm / 6'0\""),
    (184, "184 cm / 6'0\""),
    (185, "185 cm / 6'1\""),
    (186, "186 cm / 6'1\""),
    (187, "187 cm / 6'2\""),
    (188, "188 cm / 6'2\""),
    (189, "189 cm / 6'2\""),
    (190, "190 cm / 6'3\""),
    (191, "191 cm / 6'3\""),
    (192, "192 cm / 6'4\""),
    (193, "193 cm / 6'4\""),
    (194, "194 cm / 6'4\""),
    (195, "195 cm / 6'5\""),
    (196, "196 cm / 6'5\""),
    (197, "197 cm / 6'6\""),
    (198, "198 cm / 6'6\""),
    (199, "199 cm / 6'6\""),
    (200, "200 cm / 6'7\""),
    (201, "201 cm / 6'7\""),
    (202, "202 cm / 6'8\""),
    (203, "203 cm / 6'8\""),
    (204, "204 cm / 6'8\""),
    (205, "205 cm / 6'9\""),
    (206, "206 cm / 6'9\""),
    (207, "207 cm / 6'9\""),
    (208, "208 cm / 6'10\""),
    (209, "209 cm / 6'10\""),
    (210, "210 cm / 6'11\""),
    (211, "> 210 cm / 6'11\""),
)

WEIGHT_CHOICE = (
    (0, ''),
    (40, '40 kg / 88 lbs'),
    (41, '41 kg / 90 lbs'),
    (42, '42 kg / 93 lbs'),
    (43, '43 kg / 95 lbs'),
    (44, '44 kg / 97 lbs'),
    (45, '45 kg / 99 lbs'),
    (46, '46 kg / 101 lbs'),
    (47, '47 kg / 104 lbs'),
    (48, '48 kg / 106 lbs'),
    (49, '49 kg / 108 lbs'),
    (50, '50 kg / 110 lbs'),
    (51, '51 kg / 112 lbs'),
    (52, '52 kg / 115 lbs'),
    (53, '53 kg / 117 lbs'),
    (54, '54 kg / 119 lbs'),
    (55, '55 kg / 121 lbs'),
    (56, '56 kg / 123 lbs'),
    (57, '57 kg / 126 lbs'),
    (58, '58 kg / 128 lbs'),
    (59, '59 kg / 130 lbs'),
    (60, '60 kg / 132 lbs'),
    (61, '61 kg / 134 lbs'),
    (62, '62 kg / 137 lbs'),
    (63, '63 kg / 139 lbs'),
    (64, '64 kg / 141 lbs'),
    (65, '65 kg / 143 lbs'),
    (66, '66 kg / 146 lbs'),
    (67, '67 kg / 148 lbs'),
    (68, '68 kg / 150 lbs'),
    (69, '69 kg / 152 lbs'),
    (70, '70 kg / 154 lbs'),
    (71, '71 kg / 157 lbs'),
    (72, '72 kg / 159 lbs'),
    (73, '73 kg / 161 lbs'),
    (74, '74 kg / 163 lbs'),
    (75, '75 kg / 165 lbs'),
    (76, '76 kg / 168 lbs'),
    (77, '77 kg / 170 lbs'),
    (78, '78 kg / 172 lbs'),
    (79, '79 kg / 174 lbs'),
    (80, '80 kg / 176 lbs'),
    (81, '81 kg / 179 lbs'),
    (82, '82 kg / 181 lbs'),
    (83, '83 kg / 183 lbs'),
    (84, '84 kg / 185 lbs'),
    (85, '85 kg / 187 lbs'),
    (86, '86 kg / 190 lbs'),
    (87, '87 kg / 192 lbs'),
    (88, '88 kg / 194 lbs'),
    (89, '89 kg / 196 lbs'),
    (90, '90 kg / 198 lbs'),
    (91, '91 kg / 201 lbs'),
    (92, '92 kg / 203 lbs'),
    (93, '93 kg / 205 lbs'),
    (94, '94 kg / 207 lbs'),
    (95, '95 kg / 209 lbs'),
    (96, '96 kg / 212 lbs'),
    (97, '97 kg / 214 lbs'),
    (98, '98 kg / 216 lbs'),
    (99, '99 kg / 218 lbs'),
    (100, '100 kg / 220 lbs'),
    (101, '101 kg / 223 lbs'),
    (102, '102 kg / 225 lbs'),
    (103, '103 kg / 227 lbs'),
    (104, '104 kg / 229 lbs'),
    (105, '105 kg / 231 lbs'),
    (106, '106 kg / 234 lbs'),
    (107, '107 kg / 236 lbs'),
    (108, '108 kg / 238 lbs'),
    (109, '109 kg / 240 lbs'),
    (110, '110 kg / 243 lbs'),
    (111, '111 kg / 245 lbs'),
    (112, '112 kg / 247 lbs'),
    (113, '113 kg / 249 lbs'),
    (114, '114 kg / 251 lbs'),
    (115, '115 kg / 254 lbs'),
    (116, '116 kg / 256 lbs'),
    (117, '117 kg / 258 lbs'),
    (118, '118 kg / 260 lbs'),
    (119, '119 kg / 262 lbs'),
    (120, '120 kg / 265 lbs'),
    (121, '121 kg / 267 lbs'),
    (122, '122 kg / 269 lbs'),
    (123, '123 kg / 271 lbs'),
    (124, '124 kg / 273 lbs'),
    (125, '125 kg / 276 lbs'),
    (126, '126 kg / 278 lbs'),
    (127, '127 kg / 280 lbs'),
    (128, '128 kg / 282 lbs'),
    (129, '129 kg / 284 lbs'),
    (130, '130 kg / 287 lbs'),
)

DIET_CHOICE = (
    (0, ''),
    (1, _('anything')),
    (2, _('balanced')),
    (3, _('lots of meat')),
    (5, _('mostly vegetarian')),
    (6, _('strictly vegetarian')),
    (7, _('mostly vegan')),
    (8, _('strictly vegan')),
    (9, _('mostly kosher/halal')),
    (10, _('strictly kosher/halal')),
)

JOBFIELD_CHOICE = (
    (0, ''),
    (1, _('administration')),
    (2, _('art')),
    (3, _('banking')),
    (4, _('construction')),
    (5, _('education')),
    (6, _('engineering')),
    (7, _('entertainment')),
    (8, _('government')),
    (9, _('hospitality')),
    (10, _('internet')),
    (11, _('law')),
    (12, _('medicine')),
    (13, _('marketing')),
    (14, _('military')),
    (15, _('finance')),
    (16, _('management')),
    (17, _('music')),
    (18, _('politics')),
    # (19, _('retired')),
    (20, _('sales')),
    (21, _('science')),
    # (22, _('self-employed')),
    # (23, _('student')),
    (24, _('technology')),
    # (25, _('trainee')),
    (26, _('transportation')),
    # (27, _('unemployed')),
    (28, _('writing')),
    (90, _('other')),
)

INCOME_CHOICE = (
    (0, ''),
    (1, '< $10,000'),
    (2, '$10,000 - $30,000'),
    (3, '$30,000 - $60,000'),
    (5, '$60,000 - $100,000'),
    (6, '> $100,000'),
)
