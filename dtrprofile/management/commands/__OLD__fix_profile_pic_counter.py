# -*- encoding: utf-8 -*-

""" 
For each user profile, count the number of pictures and make sure there is a 
main profile avatar picture set.

"""

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.db import connection, transaction

from dtrprofile.models import UserProfile, UserPic
from dtrglue import utils

class Command(BaseCommand):

    def handle(self, *args, **options):

        for userprofile in UserProfile.objects.all():

            # Count the pics the user has.
            userprofile.profile_pic_counter = \
                           UserPic.objects.filter(user=userprofile.user).count()
            
            # Make sure there is a profile pic set if the user has any pics.
            if userprofile.profile_pic_counter > 0 and userprofile.pic is None:
                userprofile.pic = UserPic.objects.filter(user=userprofile.user)[0]

            userprofile.save()
            print 'User {} has {} pics.'.format(userprofile.user.id, 
                                                userprofile.profile_pic_counter)

        print '''Finally, set UserProfile.pic to one of the user's pictures.'''
        cursor = connection.cursor()
        cursor.execute(u'''UPDATE dtrprofile_userprofile pr 
                LEFT JOIN dtrprofile_userpic pi ON pr.user_id=pi.user_id 
                SET pr.pic_id=pi.id WHERE pr.pic_id IS NULL ''')

        print '''Done.'''
