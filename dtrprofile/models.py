# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

"""
Models for all user related data: profile, pic, messages, etc.


"""

import os
import re
import unicodedata
from datetime import date, datetime
from math import floor
from random import randint

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now as timezone_now
from django.utils.timezone import utc
from django.utils.translation import get_language

from image_with_thumbnail_field import ImageWithThumbsField

from dtrcity.models import City, Country, AltName
import dtr4.settings_single_choices as single_choices

# Reminder: SmallIntegerField -- safe +/-32767 in all databases.

def nowtime():
    return timezone_now
    #return datetime.utcnow().replace(tzinfo=utc)

USERFLAG_IS_ONE_WAY = False
USERFLAG_IS_TWO_WAY = True
USERFLAG_TYPES = (
    (1, 'friend',   USERFLAG_IS_TWO_WAY), # mutual, invite/confirm "friend" relationship
    (2, 'like',     USERFLAG_IS_TWO_WAY), # mutual, like and like back to get a romantic "match".
    (3, 'block',    USERFLAG_IS_ONE_WAY), # block another user so they can't see my profile or send messages anymore.
    (4, 'favorite', USERFLAG_IS_ONE_WAY), # you can only have 5 favorites at a time!
    (5, 'viewed',   USERFLAG_IS_ONE_WAY), # last time sender viewed the profile of receiver.
)
USERFLAG_TYPES_CHOICES = [(x[0], x[1]) for x in USERFLAG_TYPES]

class UserFlag(models.Model):
    """Set flags between user profiles: fav, like/match, block."""

    sender = models.ForeignKey(User, db_index=True, related_name='has_flagged')
    receiver = models.ForeignKey(User,db_index=True,related_name='was_flagged')
    flag_type = models.PositiveIntegerField(choices=USERFLAG_TYPES_CHOICES)
    # Time the flag was set.
    created = models.DateTimeField(default=nowtime())
    # Time mutual flag was set for reciprocal relations.
    confirmed = models.DateTimeField(default=None, null=True)

    class Meta:
        index_together = [['sender', 'receiver'], ['sender', 'receiver']]
        unique_together = ['sender', 'receiver', 'flag_type']

    def __init__(self, *args, **kwargs):
        super(UserFlag, self).__init__(*args, **kwargs)

    def __str__(self):
        s = 'Flag {0}: by {1} to {2} type "{3}".'
        return s.format(self.pk, self.sender.username,
                        self.receiver.username, self.flag_type)

    @classmethod # TODO: DELETE THIS??
    def get_flags(cls, user1, user2):
        return UserFlag.objects.filter(sender=user1, receiver=user2)

    @classmethod
    def last_viewed(cls, user1, user2):
        """Return date of the last "viewed" flag, or None if never."""
        f = UserFlag.objects.filter(sender=user1, receiver=user2, flag_type=5)
        if f:
            return f[0].created
        else:
            return None

    @classmethod
    def all_between_users(cls, user1, user2):
        """Return all flags between two users."""
        return UserFlag.objects.filter(Q(sender=user1, receiver=user2)|
                                       Q(sender=user2, receiver=user1))

    @classmethod
    def get_one_way_flags(cls, user1, user2):
        """Return all one-way flags between two users."""
        one_way_choices = [x[0] for x in USERFLAG_TYPES if not x[2]]
        return UserFlag.all_between_users(user1, user2)\
                       .filter(flag_type__in=one_way_choices)

    @classmethod
    def get_two_way_flags(cls, user1, user2):
        """Return all two-way flags between two users."""
        two_way_choices = [x[0] for x in USERFLAG_TYPES if x[2]]
        return UserFlag.all_between_users(user1, user2)\
                       .filter(flag_type__in=two_way_choices)

    @classmethod
    def get_flag(cls, flag_name, user1, user2):
        """Return a specific flag between two users.

        flag_name: one of the defined flag names, e.g. "like", "block".
        user1, user2: django.auth.models.User objects.

        Raise DoesNotExist exception if the flag doesn't exist.
        """
        try:
            # Find the flag name in the USERFLAG_TYPES list.
            flag_type, two_way_flag = [(x[0], x[2]) for x in
                                       USERFLAG_TYPES if x[1] == flag_name][0]
        except IndexError:
            raise AttributeError('No flag by this name.')
        # Fetch exactly one object, anything else would be an exception.
        return UserFlag.objects.get(Q(sender=user1, receiver=user2) |
                                    Q(sender=user2, receiver=user1),
                                    flag_type=flag_type)

class UserPic(models.Model):
    """Store data about uploaded user pictures."""

    user = models.ForeignKey(User, editable=False, related_name='pics')
    pic = ImageWithThumbsField(
        blank=False, default='', upload_to='raw', sizes=(
            ('s', 'cover',  75,  75),
            ('m', 'cover', 300, 300),
            ('x', 'contain', 800, 800),
        ))
    # Upload time and uploader's IP.
    created = models.DateTimeField(default=nowtime())
    created_ip = models.CharField(default='', max_length=15, blank=True)
    # TODO: Not used yet, just in case for later.
    text = models.TextField(default='', blank=True)

    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super(UserPic, self).__init__(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        """Always return empty string, never show URL of raw pic."""
        # Do not return self.pic.url here.
        return ''

    def get_filename(self):
        """Return the filename with no path, e.g. '823.jpg'."""
        return '{}.jpg'.format(self.id)

    def get_aspect_height(self, width):
        """Return the height if image was resized to 'width'."""
        cw, ch = self.pic.width, self.pic.height
        return (ch * width / cw)

    def delete(self, *args, **kwargs):
        """Delete self and all files with different image sizes."""
        self.pic.delete()
        super(UserPic, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(UserPic, self).save(*args, **kwargs)

class UserMsg(models.Model):
    """Store private messages between users."""

    from_user = models.ForeignKey(User, related_name='msg_sent',
                                  null=True, on_delete=models.SET_NULL)
    to_user = models.ForeignKey(User, related_name='msg_received',
                                null=True, on_delete=models.SET_NULL)
    # Set True when user opens profile page and messages are displayed.
    is_read = models.BooleanField(default=False)
    # Set True if user replies or manually sets it to "done".
    is_replied = models.BooleanField(default=False)
    # Set True if the sending user was blocked by receiver.
    # TODO: remove and handle in UserFlag only!
    is_blocked = models.BooleanField(default=False)
    # Time and IP the message was sent.
    created = models.DateTimeField()
    created_ip = models.CharField(default='', max_length=15, blank=True)
    # The actual text of the message.
    text = models.TextField()

    class Meta:
        index_together = [['from_user', 'to_user'], ['to_user', 'from_user']]

    def __str__(self):
        s = 'Message [{}] from "{}" ({}) to "{}" ({}) on "{}".'
        return s.format(self.id, self.from_user.username, self.from_user.id,
                        self.to_user.username, self.to_user.id, self.created)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = nowtime()
        super(UserMsg, self).save(*args, **kwargs)

    @classmethod
    def set_is_read_all(cls, to_user):
        """Set all messages received by 'to_user' to is_read=True."""
        for row in UserMsg.objects.filter(to_user=to_user, is_read=False):
            # TODO: there's a more efficient way to do this!
            # "bulk update" something.
            row.is_read = True
            row.save()

    @classmethod
    def set_is_read(cls, from_user, to_user):
        """Set all msgs by 'from_user' to 'to_user' to is_read=True."""
        for row in UserMsg.objects.filter(from_user=from_user,to_user=to_user):
            # TODO: there's a more efficient way to do this!
            # "bulk update" something.
            row.is_read = True
            row.save()

    @classmethod
    def unset_is_read(cls, from_user, to_user):
        """Sets *last* msg by from_user to to_user to is_read=False."""
        msg = UserMsg.objects.filter(from_user=from_user, to_user=to_user)\
                             .order_by('-created').first()
        if msg is not None:
            msg.is_read = False
            msg.save()

class UserProfile(models.Model):
    """All user profile info is here.

    Most fields should be integers that are used as bitmaps for
    multi-options choice fields. Try to avoid using text fields,
    the user should not have to write much about themselves.
    """

    user = models.OneToOneField(User, primary_key=True,
                                editable=False, related_name='profile')
    # When did the user last edit their profile data.
    last_modified = models.DateTimeField(default=nowtime())
    # When did the user last load a page while logged in.
    # This is automagically updated by a Middleware.
    last_active = models.DateTimeField(db_index=True, default=nowtime())
    active_counter = models.IntegerField(default=0, editable=False)

    # Settings data
    #
    # What language to show the site in.
    language = models.CharField(verbose_name='language',
                                max_length=10, default='en')
    # Receive emails about activity?
    notification_emails = models.SmallIntegerField(
        default=0, choices=single_choices.NOTIFICATION_EMAILS)
    # When was the last email sent?
    last_email = models.DateTimeField(null=True, default=None)

    # Use costum CSS when showing the profile page?
    style_active = models.BooleanField(default=False)
    style = models.TextField(verbose_name='Profile page CSS styles',
                             default='', blank=True)

    # Counter fields. Most shown in navbar.
    #
    # Count received friend invites not yet confirmed or rejected.
    friend_open_invites_recv_counter = models.IntegerField(default=0)
    # Count mutually confirmed friend relationship.
    friend_mutual_confirmed_counter = models.IntegerField(default=0)
    # Count "likes" received and not yet confirmed or rejected.
    match_open_invites_recv_counter = models.IntegerField(default=0)
    # Count matches (mutually confirmed likes).
    match_mutual_confirmed_counter = models.IntegerField(default=0)
    # Count total mails received.
    mail_recv_counter = models.IntegerField(default=0)
    # Count total mails sent. To find spammers.
    mail_sent_counter = models.IntegerField(default=0)
    # Count mails received and not read yet.
    mail_unread_counter = models.IntegerField(default=0)
    # Count how many times the profile page was viewed by other users.
    views_counter = models.IntegerField(default=0)

    # PASL data
    #
    pic = models.ForeignKey(UserPic, null=True, default=None, blank=True,
                            editable=False, on_delete=models.SET_NULL)
    dob = models.DateField(null=True, default=None, blank=True)
    gender = models.SmallIntegerField(verbose_name='gender', default=11,
                                      choices=single_choices.GENDER_CHOICE) # 11=other
    # Lat/lng in decimal degrees (wgs84)
    lat = models.FloatField(db_index=True, null=True, default=None)
    lng = models.FloatField(db_index=True, null=True, default=None)
    #
    # Name of "country" and name of nearest larger "city" to lat/lng.
    #
    # To get the actual name string, has to query "AltName" for the city ID,
    # the user's prefered language, and "main" to fetch the main name of the
    # place, rather than the alternative names.
    #
    # To search users, always get the lat/lng values from the "AltName" table
    # and then use them to find all users close to that point. Never search
    # just by city name.
    #
    # The ID of the city (because in AltNames, there are several entries for
    # each object, because they may even have more than one name in the same
    # language!) The region and country reference makes it also possible to
    # list profiles by region or country for better SEO.
    city = models.ForeignKey(City, db_index=True, blank=True, null=True,
                             default=None, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, db_index=True, blank=True, null=True,
                                default=None, on_delete=models.SET_NULL)
    # TODO: this is the OLD raw crc string, to try and filter out what
    # city  it is, so to attach a geoname_id on the city and country.
    # After that, delete it.
    crc = models.CharField(default='', editable=False, max_length=250)

    # Lots to write about

    aboutme = models.TextField(null=False, default='', blank=True)
    aboutbooks = models.TextField(null=False, default='', blank=True)
    aboutmovies = models.TextField(null=False, default='', blank=True)
    aboutmusic = models.TextField(null=False, default='', blank=True)
    aboutarts = models.TextField(null=False, default='', blank=True)
    abouttravel = models.TextField(null=False, default='', blank=True)
    aboutfood = models.TextField(null=False, default='', blank=True)
    aboutquotes = models.TextField(null=False, default='', blank=True)
    aboutsports = models.TextField(null=False, default='', blank=True)

    # All single choice fields

    lookingfor = models.SmallIntegerField(
        default=0, choices=single_choices.LOOKINGFOR_CHOICE)
    height = models.SmallIntegerField(
        default=0, choices=single_choices.HEIGHT_CHOICE)
    weight = models.SmallIntegerField(
        default=0, choices=single_choices.WEIGHT_CHOICE)
    eyecolor = models.SmallIntegerField(
        default=0, choices=single_choices.EYECOLOR_CHOICE)
    haircolor = models.SmallIntegerField(
        default=0, choices=single_choices.HAIRCOLOR_CHOICE)
    relationship_status = models.SmallIntegerField(
        default=0, choices=single_choices.RELATIONSHIP_STATUS_CHOICE)
    has_children = models.SmallIntegerField(
        default=0, choices=single_choices.HAS_CHILDREN_CHOICE)
    want_children = models.SmallIntegerField(
        default=0, choices=single_choices.WANT_CHILDREN_CHOICE)
    would_relocate = models.SmallIntegerField(
        default=0, choices=single_choices.WOULD_RELOCATE_CHOICE)
    smoke = models.SmallIntegerField(
        default=0, choices=single_choices.SMOKE_CHOICE)
    pot = models.SmallIntegerField(
        default=0, choices=single_choices.POT_CHOICE)
    drink = models.SmallIntegerField(
        default=0, choices=single_choices.DRINK_CHOICE)
    longest_relationship = models.SmallIntegerField(
        default=0, choices=single_choices.LONGEST_RELATIONSHIP_CHOICE)
    looks = models.SmallIntegerField(
        default=0, choices=single_choices.LOOKS_CHOICE)
    figure = models.SmallIntegerField(
        default=0, choices=single_choices.FIGURE_CHOICE)
    fitness = models.SmallIntegerField(
        default=0, choices=single_choices.FITNESS_CHOICE)
    education = models.SmallIntegerField(
        default=0, choices=single_choices.EDUCATION_CHOICE)
    diet = models.SmallIntegerField(
        default=0, choices=single_choices.DIET_CHOICE)
    sports = models.SmallIntegerField(
        default=0, choices=single_choices.SPORTS_CHOICE)
    religion = models.SmallIntegerField(
        default=0, choices=single_choices.RELIGION_CHOICE)
    religiosity = models.SmallIntegerField(
        default=0, choices=single_choices.RELIGIOSITY_CHOICE)
    spirituality = models.SmallIntegerField(
        default=0, choices=single_choices.SPIRITUALITY_CHOICE)
    jobfield = models.SmallIntegerField(
        default=0, choices=single_choices.JOBFIELD_CHOICE)
    income = models.SmallIntegerField(
        default=0, choices=single_choices.INCOME_CHOICE)

    # Automatically set from birth date

    western_zodiac = models.SmallIntegerField(
        editable=False, default=0,choices=single_choices.WESTERN_ZODIAC_CHOICE)
    eastern_zodiac = models.SmallIntegerField(
        editable=False, default=0,choices=single_choices.EASTERN_ZODIAC_CHOICE)

    def __str__(self):
        s = "UserProfile for {0} (#{1})"
        return s.format(self.user.id, self.user.username)

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self.language = settings.LANGUAGE_CODE[:2]
        self.age = self.get_age()
        self.crc = self.get_crc()
        self.is_online = self.get_is_online()
        self.is_idle = self.get_is_idle()
        self.is_offline = self.get_is_offline()
        self.pic_url_s = self.get_pic_url(self.pic, 's')
        self.pic_url_m = self.get_pic_url(self.pic, 'm')
        self.pic_url_x = self.get_pic_url(self.pic, 'x')

    def save(self, *args, **kwargs):
        # remember user's language setting, 2 char code only!
        # --> No, don't! Updates like view_counter would set this to the
        # other user's language setting! Needs to be updated explicitly.
        #self.language = get_language()[:2]
        # Make star signs searchable.
        if self.dob:
            self.western_zodiac = self.get_western_zodiac()
            self.eastern_zodiac = self.get_eastern_zodiac()
        super(UserProfile, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None,created=False, **kwargs):
        if created:
            UserProfile.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()

    @classmethod
    def get_pic_url(cls, pic, size='s'):
        # Try to attach the pic urls here to avoid having to hit the UserPic
        # model simply to display the profile avatar pic.
        # /[MEDIA_URL]/[size]/[int(pic_id/10000)]/[pic_id].jpg

        if isinstance(pic, UserPic): # Accept both UserPic objects and Integers.
            pic_id = pic.id
        elif isinstance(pic, int):
            pic_id = pic
        else: # If its None or something, then return a "has no picture" image.
            return os.path.join(settings.STATIC_URL, 'img/404-userpic-{}.jpg'.format(size))
        sub = str(int(floor(pic_id / 10000)))
        base = settings.MEDIA_URL.rstrip('/')
        return '{}/{}/{}/{}.jpg'.format(base, size, sub, pic_id)

    def get_absolute_url(self):
        # Return the URL path of the profile.
        return reverse('user_profile', args=[self.user.username])

    def get_crc(self):
        try:
            return AltName.objects.get(geoname_id=self.city.pk, type=3,
                                       language=(get_language() or
                                                 settings.LANGUAGE_CODE)[:2],
                                       is_main=True).crc
        except AltName.DoesNotExist:
            print('AltName "{2}" not found for City "{0}:{1}".'.format(
                self.city.pk, self.city.name,
                (get_language() or settings.LANGUAGE_CODE)[:2]
            ))
            return ''
        except AttributeError:
            return ''

    def get_gender_symbol(self):
        try:
            a = single_choices.GENDER_CHOICE_SYMBOL
            return [x[1] for x in a if x[0] == self.gender][0]
        except IndexError:
            return ''

    def get_gender_heshe(self):
        try:
            a = single_choices.GENDER_CHOICE_HESHE
            return [x[1] for x in a if x[0] == self.gender][0]
        except:
            return ''

    def get_gender_hisher(self):
        try:
            a = single_choices.GENDER_CHOICE_HISHER
            return [x[1] for x in a if x[0] == self.gender][0]
        except:
            return ''

    def get_age(self):
        try:
            delta = date.today() - self.dob
            return int(delta.days / 365)
        except:
            return ''

    def get_western_zodiac(self):
        try:
            mdd = int(self.dob.strftime('%m%d'))
            lim = single_choices.WESTERN_ZODIAC_UPPER_LIMIT
            return [e[1] for e in lim if mdd < e[0]][0]
        except:
            return 0

    def get_eastern_zodiac(self):
        try:
            ymd = int(self.dob.strftime('%Y%m%d'))
            lim = single_choices.EASTERN_ZODIAC_UPPER_LIMIT
            return [e[1] for e in lim if ymd < e[0]][0]
        except:
            return 0

    def get_western_zodiac_symbol(self):
        try:
            a = single_choices.WESTERN_ZODIAC_SYMBOLS
            return [x[1] for x in a if x[0]==self.western_zodiac][0]
        except:
            return ''

    def get_eastern_zodiac_symbol(self):
        try:
            a = single_choices.EASTERN_ZODIAC_SYMBOLS
            return [x[1] for x in a if x[0]==self.eastern_zodiac][0]
        except:
            return ''

    def get_last_active_seconds(self):
        if self.last_active is None:
            # When instantiated a new UserProfile, needs to return something.
            return 0

        dtime = datetime.utcnow().replace(tzinfo=utc)
        return (dtime - self.last_active).total_seconds()

    def get_is_online(self):
        x = settings.ONLINE_SECONDS_SINCE_LAST_ACTIVE
        return self.get_last_active_seconds() < x

    def get_is_idle(self):
        x = settings.IDLE_SECONDS_SINCE_LAST_ACTIVE
        return self.get_last_active_seconds() < x and not self.get_is_online()

    def get_is_offline(self):
        return not self.get_is_online() and not self.get_is_idle()

    def get_friends(self):
        '''
        Return list of user objects that are friends (reciprocal friends flag)
        by profile user.
        '''
        f1 = User.objects.filter(has_flagged__receiver=self.user,
                                 has_flagged__confirmed__isnull=False,
                                 has_flagged__flag_type=1)
        f2 = User.objects.filter(was_flagged__sender=self.user,
                                 was_flagged__confirmed__isnull=False,
                                 was_flagged__flag_type=1)
        return list(f1) + list(f2)


################################################################################

class Talk(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             db_index=True, related_name='talks')
    created = models.DateTimeField()
    created_ip = models.CharField(default='', max_length=15)
    parent = models.ForeignKey('self', db_index=True, null=True,
                                       default=None, related_name='children')
    child_counter = models.SmallIntegerField(default=0)
    views_counter = models.SmallIntegerField(default=0)
    hashtag_counter = models.SmallIntegerField(default=0)
    username_counter = models.SmallIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    text = models.TextField()

    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super(Talk, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.text

class TalkHashtag(models.Model):
    tag = models.CharField(max_length=50, db_index=True) # the hashtag withOUT the "#" hash.
    talk = models.ForeignKey(Talk, db_index=True, related_name="hashtag") # ref to talk post id

class TalkUsername(models.Model):
    user = models.ForeignKey(User, db_index=True, related_name="mentioned_in")
    talk = models.ForeignKey(Talk, db_index=True, related_name="mentions")
