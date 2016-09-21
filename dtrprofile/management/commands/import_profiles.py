
"""Import all user accounts and user profile data."""

from datetime import datetime

import pymysql
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import utc

import dtr4.settings_single_choices as single_choices
from dtrcity.models import City, Country
from dtrprofile.models_flag import UserFlag
from dtrprofile.models_profile import UserPic, UserProfile
from dtrprofile.models_usermsg import UserMsg

print('Beginning import of OLD elligue data.')

# Get a connect to the old elligue database.
conn = pymysql.connect( host='localhost', port=3306,
                        user='root', passwd='pla', db='elligue')
try:
    crsr = conn.cursor()
except:
    raise Exception('No database connection!')

print('OLD database "elligue" connected.')


# Run command.
class Command(BaseCommand):
    args = ''
    help = 'Imports old user profiles from "elligue" database tables.'

    def handle(self, *args, **options):
        self.import_auth_user()
        self.import_dtrprofile_userpic()
        self.import_dtrprofile_userprofile()
        self.import_dtrprofile_usermsg()
        self.import_dtrprofile_flag() # like, friend, favorite, block

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def import_auth_user(self):
        # 1. Read auth_user items from OLD and add to NEW, preserving pk value.
        # Check how many items we have in OLD and NEW auth_user tables.
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM auth_user')
        count_old = cursor.fetchone()[0]
        count_new = User.objects.count()
        print('Counted {0} in OLD, and {1} in NEW auth_user table.'.format(count_old, count_new))

        if count_old > count_new:
            print('...so find and import the missing users:')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM auth_user')

            for row in cursor:
                # Check if the user already exists.
                try:
                    user = User.objects.get(pk=row[0])
                    print('User {} already exists, not imported again.'.format(user.pk))
                except:
                    # if not, import the auth_user data and create the user.
                    user = User.objects.create_user(row[4], id=row[0], email=row[7])

                    user.password = row[1]
                    user.last_login = row[2].replace(microsecond=0).replace(tzinfo=utc)
                    user.first_name=row[5]
                    user.last_name=row[6]
                    user.date_joined = row[10].replace(microsecond=0).replace(tzinfo=utc)
                    user.save()

                    print('Added user {} to auth_user and import data.'.format(user.pk))
        else:
            print('No more users to import.')

        print('Setting "csx" as superuser done...')
        user = User.objects.get(username="csx")
        user.set_password('pla')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print('Done!')
        print('Finished auth_user table.')

    # --------------------------------------------------------------------------

    def import_dtrprofile_userpic(self):
        print('Starting import of UserPic images...')

        # Check how many items we have in OLD and NEW auth_user tables.
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dtrprofile_userpic')
        count_old = cursor.fetchone()[0]
        count_new = UserPic.objects.count()
        print('Counted {0} in OLD, and {1} in NEW UserPic table.'.format(count_old, count_new))

        if count_old > count_new:
            print('...so find and import the missing pics:')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dtrprofile_userpic')

            for row in cursor:
                # Check if the user already exists.
                try:
                    pic = UserPic.objects.get(pk=row[0])
                    print( 'UserPic {} already exists, not imported again.'.format(pic.pk) )
                except:
                    # row[0]#id       row[1]#user_id       row[2]#pic
                    # row[3]#status   row[4]#filesize      row[5]#width
                    # row[6]#height   row[7]#created       row[8]#created_ip
                    # row[9]#text     row[10]#like_count
                    pic = UserPic(id=row[0], user_id=row[1], pic=row[2],
                                  created=row[7].replace(tzinfo=utc),
                                  created_ip=row[8], text=row[9])
                    pic.save()

                    print('Added pic {} to UserPic.'.format(pic.pk))
        else:
            print('No more pics to import.')

        print('Finished dtrprofile_userpic --> UserPic table.')

    # --------------------------------------------------------------------------

    def import_dtrprofile_userprofile(self):
        print('Starting import of UserProfile data...')

        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dtrprofile_userprofile')
        count_old = cursor.fetchone()[0]
        count_new = UserProfile.objects.count()
        print('Counted {0} in OLD, and {1} in NEW dtrprofile_userprofile table.'.format(count_old, count_new))

        print('Updating or creating all profiles with imported data.')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dtrprofile_userprofile')

        for row in cursor:
            # Check if the profile already exists, else create new row.
            try:
                profile = UserProfile.objects.get(pk=row[0])
            except:
                profile = UserProfile(user_id=row[0])

            # Overwrite previous values ans save.

            # Set timezone to UTC always.
            profile.last_modified = row[7].replace(tzinfo=utc)
            profile.last_active = row[8].replace(tzinfo=utc)

            profile.language = row[5]
            profile.notification_emails = 3
            profile.style = row[3]
            profile.style_active = False

            # For pic, check if a UserPic with this ID actually exists!
            try:
                UserPic.objects.get(pk=row[1])
                profile.pic_id = row[1]
            except:
                profile.pic_id = None

            profile.dob = row[42]

            # Gender needs fixing, because now gender and orientation are combined!
            # row[45] => old gender --- row[46] => old orientation
            profile.gender = 0 # set default.
            tr_gender = ((10, 10, 1), (10, 20, 2), (10, 30, 11), (10, 40, 11),
                         (20, 10, 4), (20, 20, 5), (20, 30, 11), (20, 40, 11),
                         (30, 10, 11), (30, 20, 11),(30, 30, 11), (30, 40, 11),
                         (40, 10, 11), (40, 20, 11), (40, 30, 11), (40, 40, 11))
            for tr in tr_gender:
                if row[45] == tr[0] and row[46] == tr[1]:
                    profile.gender = tr[2]

            profile.crc = row[47] # Never used, only to try and find the city later.
            profile.lat = row[48]
            profile.lng = row[49]

            # For city and country, check if a City or Country with this
            # geoname_id actually exists!
            try:
                profile.country_id = Country.objects.get(pk=row[52]).pk # row # checked
            except:
                profile.country_id = None
            try:
                profile.city_id = City.objects.get(pk=row[50]).pk # row # checked
            except:
                profile.city_id = None

            profile.aboutme = row[54]
            profile.aboutbooks = row[55]
            profile.aboutmovies = row[56]
            profile.aboutmusic = row[57]
            profile.aboutarts = row[58]
            profile.abouttravel = row[59]
            profile.aboutfood = row[60]
            profile.aboutquotes = row[61]
            profile.aboutsports = row[62]

            # --> Check all these before import that they stay withn CHOICE range!
            if row[43] in [v[0] for v in single_choices.HEIGHT_CHOICE]:
                profile.height = row[43]
            if row[44] in [v[0] for v in single_choices.WEIGHT_CHOICE]:
                profile.weight = row[44]
            profile.eyecolor = int(row[63])/10 # Convert from 10, 20, 30, ... into 1, 2, 3, ...
            profile.haircolor = int(row[64])/10

            profile.relationship_status = int(row[65])/10
            profile.longest_relationship = int(row[72])/10
            profile.has_children = int(row[66])/10
            profile.want_children = int(row[67])/10
            profile.would_relocate = int(row[68])/10

            profile.smoke = int(row[69])/10
            profile.pot = int(row[70])/10
            profile.drink = int(row[71])/10
            profile.diet = int(row[83])/10
            profile.sports = int(row[76])/10

            profile.religion = int(row[77])/10
            profile.religiosity = int(row[79])/10
            profile.spirituality = int(row[80])/10

            profile.education = int(row[78])/10
            profile.jobfield = int(row[90])/10
            profile.income = 0

            #profile.lookingfor --> row[86]
            if row[86] == 0x0000000000000001: profile.lookingfor = 1 # friends only
            if row[86] == 0x0000000000000002: profile.lookingfor = 2 # serious relationship
            if row[86] == 0x0000000000000004: profile.lookingfor = 3 # casual dating
            if row[86] == 0x0000000000000008: profile.lookingfor = 4 # passion
            if row[86] == 0x0000000000000010: profile.lookingfor = 5 # casual sex
            if row[86] == 0x0000000000000020: profile.lookingfor = 6 # not sure yet
            if row[86] == 0x0000000000000040: profile.lookingfor = 7 # marriage

            #looks = row[73]
            #figure = row[74]
            #fitness = row[75]
            #speaks_languages = row[87]
            #ethnicity = row[88]
            #political_ideology = row[89]

            profile.save()
            print('New profile {} created or udated with imported data.'.format(profile.pk))

        print('Finished dtrprofile_userprofile table.')

    # --------------------------------------------------------------------------

    def import_dtrprofile_usermsg(self):
        print('Starting import of UserMsg data...')

        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dtrprofile_usermsg')
        count_old = cursor.fetchone()[0]
        count_new = UserMsg.objects.count()
        i, todo = 0, (count_old - count_new)
        print('Counted {0} in OLD, and {1} in NEW dtrprofile_usermsg table.'.format(count_old, count_new))

        if count_old > count_new:
            print('...so find and import the missing msgs:')

            # Fetch the last imported message's pk
            try:
                pk = UserMsg.objects.all().order_by('pk').last().pk
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM dtrprofile_usermsg WHERE id > {0}'.format(pk))
            except:
                cursor.execute('SELECT * FROM dtrprofile_usermsg')

            # 0 | id           | int(11)     | NO   | PRI | NULL    | auto_increment |
            # 1 | from_user_id | int(11)     | YES  | MUL | NULL    |                |
            # 2 | to_user_id   | int(11)     | YES  | MUL | NULL    |                |
            # 3 | status       | smallint(6) | NO   | MUL | NULL    |                |
            # 4 | created      | datetime    | NO   |     | NULL    |                |
            # 5 | created_ip   | char(15)    | NO   |     | NULL    |                |
            # 6 | text         | longtext    | NO   |     | NULL    |                |

            for row in cursor:
                i = i + 1
                msg = UserMsg(pk=row[0])

                # check if it was not deleted by receiver
                # 0x0001 --> from_deleted ; 0x0002 --> to_deleted
                if not (row[3] & 0x0002): # row[3] == status
                    # Try to fetch users.
                    try:
                        from_user = User.objects.get(pk=row[1])
                    except User.DoesNotExist:
                        from_user = None
                    try:
                        to_user = User.objects.get(pk=row[2])
                    except User.DoesNotExist:
                        to_user = None

                    msg.from_user = from_user
                    msg.to_user = to_user
                    msg.is_read = True
                    msg.is_replied = True
                    msg.created = row[4].replace(tzinfo=utc)
                    msg.created_ip = row[5]
                    msg.text = row[6]
                    msg.save()

                print('{1}/{2} - added msg id {0}.'.format(msg.pk, i, todo))

        print('Finished dtrprofile_usermsg table.')

    # --------------------------------------------------------------------------

    def import_dtrprofile_flag(self):
        print('Starting import of UserFlag data...')
        print('Flags have to be converted, there is no way to count-and-compare them.')
        print('Each time we need to trunate the new table and start over.')
        UserFlag.objects.all().delete()
        print('All NEW UserFlag data deleted for fresh import.')

        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dtrflag_flag WHERE otype=2') # only flags on profiles
        count_old = cursor.fetchone()[0]
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dtrflag_flag WHERE otype=2 ORDER BY id ASC') # only flags on profiles
        i = 0 # rows worked on
        j = 0 # individual flags imported.

        for row in cursor:
            i = i + 1
            print('{0}/{1} ~ '.format(i, count_old), end='', flush=True)

            try:
                sender = User.objects.get(pk=row[1])
                receiver = User.objects.get(pk=row[4])
            except User.DoesNotExist:
                print('user not found, skip entry.', flush=True)
                continue # skip if either user does not exist.

            print('{0} -> {1} ~ '.format(sender.pk, receiver.pk), end='', flush=True)

            # All this needs to be converted, differently for every FLAG TYPE!
            # 1--friend ------- 0x0100 ( NOT 2 )
            # 2--like --------- 0x0010 ( NOT 1 )
            # 3--favourite ---- 0x0200 -- NO ENTRIES, SKIP!
            # 4--block -------- 0x0080

            if row[5] & 0x0080: # block - 4
                print('"block" flag found! ', end='', flush=True)
                flag = UserFlag(sender=sender, receiver=receiver, flag_type=4)
                print('user {0} BLOCKED by user {1}, skip other flags.'.format(
                                receiver.username, sender.username), flush=True)
                j = j + 1
                continue # blocked is blocked, no other relationship possible.

            if row[5] & 0x0010: # like - 2
                print('"like" flag found... ', end='', flush=True)
                # This is a reciprocal flag, so first check if there is already
                # a flag set coming the otehr way!
                try:
                    # Roles reversed!
                    flag = UserFlag.objects.get(sender=receiver,
                                                receiver=sender, flag_type=2)
                    flag.confirmed = datetime.utcnow().replace(tzinfo=utc)
                    flag.save()
                    print('this was a MATCH! ', end='', flush=True)
                except:
                    # Roles straight again.
                    flag = UserFlag.objects.create(sender=sender,
                                                 receiver=receiver, flag_type=2)
                    print('added! ', end='', flush=True)
                # Count flags added.
                j = j + 1

            if row[5] & 0x0100: # friend - 1
                print('"friend" flag found! ', end='', flush=True)
                # Again, check for reciprocal.
                try:
                    # Roles reversed!
                    flag = UserFlag.objects.get(sender=receiver,
                                                receiver=sender, flag_type=1)
                    flag.confirmed = datetime.utcnow().replace(tzinfo=utc)
                    flag.save()
                    print('confirmed friends! ', end='', flush=True)
                except:
                    # Roles straight again.
                    flag = UserFlag.objects.create(sender=sender,
                                                 receiver=receiver, flag_type=1)
                    print('friend invite added! ', end='', flush=True)
                # Count flags added.
                j = j + 1

            print(' done!', flush=True)

            # dtrflag_flag
            # ------------------------------------------------------------
            # 0 | id       | int(11)              | NO   | PRI | NULL    |
            # 1 | user_id  | int(11)              | NO   | MUL | NULL    |
            # 2 | otype    | smallint(5) unsigned | NO   |     | NULL    |
            # 3 | oid      | int(10) unsigned     | NO   | MUL | NULL    |
            # 4 | ouser_id | int(11)              | YES  | MUL | NULL    |
            # 5 | flags    | int(10) unsigned     | NO   |     | NULL    |
            # 6 | created  | datetime             | NO   |     | NULL    |
            # 7 | text     | varchar(250)         | NO   |     | NULL    |

        print('All done.')
        print('Finished dtrprofile_userflag table.')

    # --------------------------------------------------------------------------



