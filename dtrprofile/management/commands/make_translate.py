# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

"""Make JS translation files for profile choices and tr() calls.

   --------------------------------------------------------------------------
--> TODO: Need to manually copy the resulting files over to the dtr4-ui app! <--
   --------------------------------------------------------------------------

Profile choices: From the user profile options defined in
    "settings_single_choices.py", create language specific javascript JSON
    files for all languages defined in the settings.LANGUAGES setting.

    The resulting JSON file for the currently set language is then
    imported by the client side app, so that profile choices can be
    displayed in the set local language.

    Attention: The LANGUAGE_CODE in settings.py has to be set to "en"
    for the translations to work!

Inline tr() calls: Search in all HTML template files for occurences of
    tr() calls to translate text. The resulting text strings ("msgid" as
    in gettext) are written to "./dtrprofile/static/tr-language-XX.js"
    with XX being the specific language code the file will be used for.
    A file is created for each language defined in "settings.LANGUAGES".

    To translate, open a "./dtrprofile/static/tr-language-XX.js" file
    and write translation strings into each "msgstr" field. It is not
    necessary to run any compilation like in gettext, the files will be
    loaded directly from the "/static/tr-language-XX.js" URL path as a
    JSON file.

    Example for tr() calls in HTML templates:
    -----------------------------------------
    tr("Hello, world!")
    tr('Hello, other world!')
    tr("Hello, {0} {1} world!", ["Wayne's", "other"])

    Example for $rootScope/$scope.tr() calls in controllers:
    --------------------------------------------------------
    $scope.tr("Hello, world!")
    $scope.tr('Hello, other world!')
    $scope.tr("Hello, {0} {1} world!", ["Wayne's", "other"])
"""

import codecs
import json
import os.path
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

import dtr4.settings_single_choices as single_choices


# noinspection PyPep8Naming
class Command(BaseCommand):

    args = ""
    help = __doc__

    def handle(self, *args, **options):
        print('Languages: {0}'.format(', '.join([x[0] for x in
                                                 settings.LANGUAGES])))
        # Complite re to lookup tr() strings.
        RE_TR_STRINGS = re.compile(r"\Wtr\(('|\")(.+?)\1(\s*,\s*\[.+?\])?\)")
        CH_PREPEND = ""  # This is now plain JSON to be loaded via JS fetch().
        TR_PREPEND = "window.TR_LANGUAGE = "

        for lang in settings.LANGUAGES:
            code, name = lang[0], lang[1]
            appdir =os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            appstatic = os.path.join(appdir, 'static')
            print('Processing language "{0}" ({1}) .'.format(code, name))

            # Make the "tr-choices-LL.js" file.

            outfile = os.path.join(appstatic, 'tr-choices-{0}.js'.format(code))
            tr_choices = {}
            with translation.override(code):  # switch language temporarily
                for tr in single_choices.JS_TRANSLATIONS_CHOICES:
                    tr_choices[tr] = []

                    for choice in getattr(single_choices, tr):
                        print("Choice '{}' has type '{}'".format(
                            choice[1], type(choice[1])))

                        if choice[1] == '': # skip empty
                            continue

                        # translate to current language from English.
                        translated = translation.ugettext(choice[1])
                        tr_item = (choice[0], translated)
                        tr_choices[tr].append(tr_item)
                        print('TR {}: {} --> {}'.format(
                            translation.get_language(), choice, tr_item))

            with codecs.open(outfile, 'w', encoding="utf-8") as fh:
                msgout = json.dumps(tr_choices, ensure_ascii=False)
                fh.write(CH_PREPEND + msgout)
            print('Done "choices".')

            # Make the "tr-language-LL.js" file.
            # TR_LANGUAGE=[ {'msgid':'profile','msgstr':'perfil'}, ... ]

            outfile = os.path.join(appstatic, 'tr-language-{0}.js'.format(code))
            ngappdir = os.path.join(settings.BASE_DIR, "ng-app")
            files = [os.path.join(ngappdir, "index.html"),
                     os.path.join(ngappdir, "dtr-controllers.js")] + \
                    [os.path.join(ngappdir, 'tpl', f) for f in
                     os.listdir(os.path.join(ngappdir, 'tpl'))
                     if f.endswith('.html')]

            # Parse files and build the raw msgid list.
            msglist, filecount = [], 0
            for fn in files:
                filecount += 1
                with open(fn, 'r') as fh:
                    for ln in fh:
                        m = RE_TR_STRINGS.search(ln)
                        if m and m.group(2) not in msglist:
                            msglist.append(m.group(2))
                            # if m.group(3) is not None: print(m.groups())

            st = 'Found {} tr strings in {} html files.'
            print(st.format(len(msglist), filecount))
            # print(msglist)
            # If a translations files already exists, read its content
            # to avoid overwriting any existing translations.
            try:
                with codecs.open(outfile, 'r', encoding="utf-8") as fh:
                    currlist = json.loads(fh.read().replace(TR_PREPEND, ""))
                    print("Found tr file with {} items.".format(len(currlist)))
            except ValueError as e:  # Nothing to JSON decode
                currlist = []
                print("No current translations file found.")

            # Merge:
            #
            # 1. Remove any entries from tr file that were not found
            #    again in the newly parsed list.
            #
            # 2. Preserve any translations already done, that means if
            #    msgid and msgstr are different
            msgdictlist = []
            tr_preserved_count = 0

            for msg in msglist:
                item = {'msgid':msg,'msgstr':msg}
                # Now check if there is a translation for this already
                # in currlist.
                for curr in currlist:
                    if item['msgid'] == curr['msgid']:
                        # Found the item, now check for a translation.
                        if curr['msgid'] != curr['msgstr']:
                            item['msgstr'] = curr['msgstr']
                            tr_preserved_count += 1
                # Finally, add the item to the list of translation dicts.
                msgdictlist.append(item)

            # Build the output dict.
            st = 'Preserved {0} existing translations.'
            print(st.format(tr_preserved_count))
            msgout = json.dumps(msgdictlist, ensure_ascii=False, indent=0)
            with codecs.open(outfile, 'w', encoding="utf-8") as fh:
                fh.write(TR_PREPEND + msgout)
            print('Done finding tr() in {0} html files.'.format(filecount))

        print('All Javascript translaton files created.')
