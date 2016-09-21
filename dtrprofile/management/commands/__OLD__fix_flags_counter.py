# -*- encoding: utf-8 -*-

'''
Count all different one-way flags each user received, 
e.g. "report", "like", etc.

'''

from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from dtrprofile.models_usermsg import UserMsg
from dtrprofile.models_profile import UserProfile
from dtrflag.models import Flag
from dtrglue import utils

class Command(BaseCommand):

    def handle(self, *args, **options):

        # These are the flags we are counting.
        report_flag_id = Flag.get_flag_id('report')
        like_flag_id = Flag.get_flag_id('like')

        # Loop through all user profiles.
        for userprofile in UserProfile.objects.all().prefetch_related('user'):

            # Loop through all flags the this user received.
            for f in Flag.objects.filter(ouser=userprofile.user):
                # The object type of the current flag.
                otype_name = Flag.get_otype_name(f.otype)

                # Check for each flag and on what otype it was set.
                if f.flags & like_flag_id:
                    if otype_name == 'dtrprofile.models.UserProfile':
                        userprofile.like_profile_counter += 1
                    elif otype_name == 'dtrprofile.models.UserPic':
                        userprofile.like_profile_pic_counter += 1
                    elif otype_name == 'dtrforum.models.Post':
                        userprofile.like_forum_post_counter += 1
                    elif otype_name == 'dtrqa.models.Answer':
                        userprofile.like_qa_post_counter += 1
                    elif otype_name == 'dtrprofile.models.UserStatus':
                        userprofile.like_user_status_post_counter += 1

                if f.flags & report_flag_id:
                    if otype_name == 'dtrprofile.models.UserProfile':
                        userprofile.report_profile_counter += 1
                    elif otype_name == 'dtrprofile.models.UserPic':
                        userprofile.report_profile_pic_counter += 1
                    elif otype_name == 'dtrforum.models.Post':
                        userprofile.report_forum_post_counter += 1
                    elif otype_name == 'dtrqa.models.Answer':
                        userprofile.report_qa_post_counter += 1
                    elif otype_name == 'dtrprofile.models.UserStatus':
                        userprofile.report_user_status_post_counter += 1

            # Save counts.
            userprofile.save()

            # Show activity.
            print 'User: {} -- Likes: profile: {} - pic: {} - forum post: {} - qa post: {} - user status: {}'.format(
                userprofile.user.id, 
                userprofile.like_profile_counter, 
                userprofile.like_profile_pic_counter, 
                userprofile.like_forum_post_counter, 
                userprofile.like_qa_post_counter, 
                userprofile.like_user_status_post_counter )
            print '         -- Report: profile: {} - pic: {} - forum post: {} - qa post: {} - user status: {}'.format(
                userprofile.report_profile_counter, 
                userprofile.report_profile_pic_counter, 
                userprofile.report_forum_post_counter, 
                userprofile.report_qa_post_counter, 
                userprofile.report_user_status_post_counter )
