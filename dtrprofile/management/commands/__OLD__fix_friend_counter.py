# -*- encoding: utf-8 -*-

'''
Count all friends, open friend invites sent, and open friend invites received 
for each user.
'''

from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from dtrflag.models import Flag
from dtrglue import utils
from dtrprofile.models import UserProfile
from dtrprofile.views import get_user_friend_invites_received, \
                             get_user_friend_invites_sent, \
                             get_user_friends

class Command(BaseCommand):

    def handle(self, *args, **options):
       
        otype = Flag.get_otype_id('dtrprofile.models.UserProfile')
        flag = Flag.get_flag_id('friend')

        for user in User.objects.all():
            count_recv = len(get_user_friend_invites_received(user, 5000))
            count_sent = len(get_user_friend_invites_sent(user, 5000))
            count_friends = len(get_user_friends(user, 5000))

            print '\rUser: {} has {} friends'.format(user.id, count_friends),
            if count_recv > 0:
                print 'and {} received open friend invites'.format(count_recv),
            if count_sent > 0:
                print 'and {} sent open friend invites'.format(count_sent),
            print '                                                      ',
            if count_recv > 0 or count_sent > 0 or count_friends > 0: print

            try: up = UserProfile.objects.get(pk=user)
            except: continue
            up.friend_counter = count_friends
            up.friend_open_invites_recv_counter = count_recv
            up.friend_open_invites_sent_counter = count_sent
            up.save()

