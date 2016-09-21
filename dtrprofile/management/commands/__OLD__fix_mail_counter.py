# -*- encoding: utf-8 -*-

'''
Count all mails sent, mails received, and unread received mails for each user.
'''

from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from dtrprofile.models_usermsg import UserMsg
from dtrprofile.models_profile import UserProfile
from dtrglue import utils

class Command(BaseCommand):

    def handle(self, *args, **options):

        to_deleted_id = UserMsg.get_status_id('to_deleted')
        from_deleted_id = UserMsg.get_status_id('from_deleted')
        is_read_id = UserMsg.get_status_id('is_read')

        for userprofile in UserProfile.objects.all():
            # Count unread msgs.
            sql = ''' SELECT COUNT(*) FROM dtrprofile_usermsg 
                      WHERE to_user_id=%s AND NOT (status & %s) '''
            cursor = connection.cursor()
            cursor.execute(sql, (userprofile.user.id, to_deleted_id) )
            userprofile.mail_unread_counter = cursor.fetchone()[0]

            # Count recv'ed msgs.
            sql = ''' SELECT COUNT(*) FROM dtrprofile_usermsg 
                      WHERE to_user_id=%s AND NOT (status & %s) '''
            cursor = connection.cursor()
            cursor.execute(sql, (userprofile.user.id, to_deleted_id) )
            userprofile.mail_recv_counter = cursor.fetchone()[0]
            
            # Count sent msgs.
            sql = ''' SELECT COUNT(*) FROM dtrprofile_usermsg 
                      WHERE from_user_id=%s AND NOT (status & %s) '''
            cursor = connection.cursor()
            cursor.execute(sql, (userprofile.user.id, from_deleted_id) )
            userprofile.mail_sent_counter = cursor.fetchone()[0]

            # Save counts.
            userprofile.save()

            # Show activity.
            print '\rUser: {} has {} unread'.format(userprofile.user.id, userprofile.mail_unread_counter),
            if userprofile.mail_recv_counter > 0:
                print ' and {} received'.format(userprofile.mail_recv_counter),
            if userprofile.mail_sent_counter > 0:
                print ' and {} sent messages'.format(userprofile.mail_sent_counter),
            print '                                                      ',
            if userprofile.mail_sent_counter > 0 \
            or userprofile.mail_recv_counter > 0 \
            or userprofile.mail_unread_counter > 0: 
                print
