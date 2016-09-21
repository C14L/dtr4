# -*- encoding: utf-8 -*-

# Import all mail and chat msgs between users.
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

from dtrprofile.models_usermsg import UserMsg
from dtrglue import utils

IMPORT_MAIL_FROM_ROW = 1 # Start row within the time limit.
IMPORT_MAIL_COUNT = 10000000 # Number of rows in each table to read.
IMPORT_MAIL_AGE = 3 # Max age of mail to import (years)


# Get a connect to the old elligue database.
try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="pla",
                           db="usr_web1_1", charset="latin1")
    crsr = conn.cursor(MySQLdb.cursors.DictCursor)
except:
    raise Exception(u'No database connection!')

ONE_YEAR = 31536000      # One year in seconds.
IMPORT_MAIL_AGE_SECONDS = IMPORT_MAIL_AGE * ONE_YEAR


# Run command.
class Command(BaseCommand):
    args = ''
    help = u'Imports user mails from El Ligue v3 database tables on "usr_web1_1".'

    def handle(self, *args, **options):

        print u'Delete everything from UserMsg...'
        msgs = UserMsg.objects.all()
        msgs.delete()
        print u'Table deleted?'
        print u'There are [{}] rows in UserMsg.'.format(UserMsg.objects.all().count())

        # Only import mails+msgs for already imported profiles!!!
        print 'Reading existing users...'
        user_ids = [str(x) for x in User.objects.filter(is_active=True).order_by('id').values_list('id', flat=True)]
        print u'Reading old mail for {} users, joining "usermails" and "usermsgs".'.format(len(user_ids))
        print 'Examples: {} {} {} {} {}'.format(user_ids[0], user_ids[5], user_ids[12], user_ids[32], user_ids[45], )
        user_ids_list = u','.join(user_ids)

        sql = u'''
            SELECT * FROM 
            ((
                SELECT
                    `m`.`to_uid` AS `to_user_id`,
                    `m`.`from_uid` AS `from_user_id`,
                    `m`.`time_sent` AS `created`,
                    `m`.`text` AS `text`,
                    `m`.`deleted_by_recipient` AS `to_deleted`,
                    `m`.`deleted_by_sender` AS `from_deleted`
                FROM `usermails` `m` 
                WHERE m.to_uid IN ({}) AND m.from_uid IN ({})
                AND (`m`.`deleted_by_recipient`="0" OR `m`.`deleted_by_sender`="0")
                AND `m`.`time_sent` > FROM_UNIXTIME( UNIX_TIMESTAMP() - %s )
                ORDER BY `m`.`msgid` ASC LIMIT %s, %s
            ) UNION (
                SELECT 
                    `u2`.`uid` AS `to_user_id`,
                    `u1`.`uid` AS `from_user_id`,
                    FROM_UNIXTIME(`time_sent`) AS `created`,
                    `m`.`text` AS `text`,
                    `m`.`deleted_by_recipient` AS `to_deleted`,
                    `m`.`deleted_by_sender` AS `from_deleted`
                FROM `usermsgs` `m`
                LEFT JOIN `userdata` `u1` ON `u1`.`nick`=`m`.`from_nick`
                LEFT JOIN `userdata` `u2` ON `u2`.`nick`=`m`.`to_nick`
                WHERE u2.uid IN ({}) AND u1.uid IN ({})
                AND (`m`.`deleted_by_recipient`="0" OR `m`.`deleted_by_sender`="0")
                AND `m`.`time_sent` > ( UNIX_TIMESTAMP() - %s )
                ORDER BY `m`.`msgid` ASC LIMIT %s, %s
            )) `all` ORDER BY `created` ASC
        '''.format(user_ids_list, user_ids_list, user_ids_list, user_ids_list)

        crsr.execute(sql % (IMPORT_MAIL_AGE_SECONDS, IMPORT_MAIL_FROM_ROW, IMPORT_MAIL_COUNT, 
                            IMPORT_MAIL_AGE_SECONDS, IMPORT_MAIL_FROM_ROW, IMPORT_MAIL_COUNT))

        counter_imported = counter_skipped = 0

        for row in crsr.fetchall():
            print u'{} | {} | {} >> Importing mail from [{}] to [{}] on "{}".'.format(
                         (counter_imported + counter_skipped), 
                         counter_imported, counter_skipped,
                         row['from_user_id'], row['to_user_id'], row['created'])

            created = row['created'].replace(tzinfo=utc)
            try:
                from_user = User.objects.get(pk=row['from_user_id'])
                to_user = User.objects.get(pk=row['to_user_id'])
            except:
                print 'User not found, skipping this message.'
                counter_skipped = counter_skipped + 1
                continue

            msg = UserMsg(from_user=from_user, 
                          to_user=to_user, 
                          created=created,
                          created_ip='0.0.0.0', # no ip info available.
                          text=row['text'])
            if row['to_deleted'] > 0: msg.receipient_delete()
            if row['from_deleted'] > 0: msg.sender_delete()
            msg.save()
            counter_imported = counter_imported + 1

        print u'Finished importing [{}] mails, and [{}] mail skipped.'.format(
                                              counter_imported, counter_skipped)




