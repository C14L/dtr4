
''' Re-create all sizes for all user pictures. '''

import json
import os.path
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File

from dtrprofile.models import UserPic

class Command(BaseCommand):
    args = ''
    help = 'Re-create all sizes for all user pictures.'

    def handle(self, *args, **options):

        print('Re-create all sizes for all user pictures.');
        print('    !! THIS WILL TAKE A LONG TIME !!');
        print('------------------------------------------');
        print('Takes each registered user pic from the UserPic model,');
        print('finds it raw/ file, and re-creates all registered picture');
        print('sizes.');
        print('');

        pics = UserPic.objects.all()
        pics_count = pics.count()
        err_pics = []
        x = '{1}/{2} - File {0}'
        i = 0

        print('Found {} pictures to process...'.format(pics_count));
        print('');
        for pic in pics:
            i += 1
            pic_filename = '{}.jpg'.format(pic.id)
            print(x.format(pic_filename, i, pics_count), end=" ");
            try:
                pic.pic.recreate(pic_filename)
            except:
                print('YO, ERROR!');
                err_pics.append(pic)
            print('done.');

        print('All done, with {0} errors:'.format(err_pics));
        print(err_pics);
        print('')
        print('')
