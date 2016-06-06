# -*- encoding: utf-8 -*-

# For each row in the User() model, import all their friends relations to other
# rows that exist in the User() model. Do not import relations to non-existant
# users.
#
# REQUIRES: import_profiles.py must be run frist!
#
# TODO 2014-03-16 WORK-IN-PROGRESS

import MySQLdb, os.path, csv, sys, re, unicodedata, time

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.db import connection, transaction
from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.html import strip_tags
from django.utils.timezone import utc

from dtrflag.models import Flag
from dtrglue import utils

IMPORT_FROM_ROW = 1
IMPORT_MAx_ROWS = 10000000

# Get a connect to the old elligue database.
conn = MySQLdb.connect(host="localhost", user="root", passwd="pla", db="usr_web1_1", charset="latin1")
crsr = conn.cursor(MySQLdb.cursors.DictCursor)

class Command(BaseCommand):
    args = ''
    help = u'For each row in the User() model, import all their friends relations to other rows that exist in the User() model. Do not import relations to non-existant users.'

    def handle(self, *args, **options):

        count = 0
        print u'Delete all the "friend" flags...'
        for flag in Flag.objects.all():
            count = count + 1
            flag.unset_flag('friend')
            flag.save()
            print "{} friend flags removed.     \r".format(count),
        print
        print u'Now reading all users and start to import the friends of each.'

        otype = Flag.get_otype_id('dtrprofile.models.UserProfile')
        count_users = 0
        count_invites = 0
        count_friendships = 0

        for user in User.objects.all(): #User.objects.filter(id=3902):
            count_users = count_users + 1
            print u'{}. -- user: {} --'.format(count_users, user.id)

            sql = u'''SELECT uid_1, uid_2, time_confirmed 
                    FROM `userfriends` 
                    WHERE ( uid_1=%s OR uid_2=%s )
                    AND time_requested > "0000-00-00 00:00:00"
                    AND time_rejected = "0000-00-00 00:00:00" '''
            crsr.execute(sql % (user.id, user.id, ))

            this_counter = 0
            for row in crsr.fetchall():
                this_counter = this_counter + 1

                # Check if the other user actually exists, if not skip row.
                if row['uid_2'] == user.id: uid = row['uid_1']
                else: uid = row['uid_2']
                try: friend = User.objects.get(pk=uid)
                except: continue

                # Confirmed or open?
                if ( row['time_confirmed'] is None ):

                    # If just an invite, we need to find who sent it.
                    count_invites = count_invites + 1
                    if row['uid_1'] == user.id: # I sent it
                        print u'Friend invite sent from user "{}" to user "{}".'.format(user.id, friend.id)
                        rel, created = Flag.objects.get_or_create(user=user, ouser=friend, oid=friend.id, otype=otype)
                    elif row['uid_1'] == friend.id: # They sent it.
                        print u'Friend invite sent from user "{}" to user "{}".'.format(friend.id, user.id)
                        rel, created = Flag.objects.get_or_create(user=friend, ouser=user, oid=user.id, otype=otype)
                    else: continue # Wtf, not possible
                    rel.set_flag('friend').save()

                else:

                    # If confirmed, we simply set the two Flags.
                    count_friendships = count_friendships + 1
                    print u'{}. Adding friendship between users "{}" and "{}".'.format(this_counter, user.id, friend.id)

                    rel, created = Flag.objects.get_or_create(user=user, 
                                       otype=otype, ouser=friend, oid=friend.id)
                    rel.set_flag('friend')
                    rel.save()

                    rel, created = Flag.objects.get_or_create(user=friend, 
                                       otype=otype, ouser=user, oid=user.id)
                    rel.set_flag('friend')
                    rel.save()

        print u'For [{}] users, imported [{}] friendships and [{}] friend invites.'.format(
                                count_users, count_friendships, count_invites)


