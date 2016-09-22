from datetime import date, datetime
from math import floor

import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import utc
from django.utils.translation import get_language

from dtr4 import settings_single_choices as single_choices
from dtrcity.models import City, Country, AltName
from dtrprofile.utils import nowtime
from image_with_thumbnail_field import ImageWithThumbsField


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

    # noinspection PyMethodMayBeStatic
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
        return ch * width / cw

    def delete(self, *args, **kwargs):
        """Delete self and all files with different image sizes."""
        self.pic.delete()
        super(UserPic, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(UserPic, self).save(*args, **kwargs)


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
    gender = models.SmallIntegerField(  # 11=other
        verbose_name='gender', default=11, choices=single_choices.GENDER_CHOICE)
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
        editable=False, default=0, choices=single_choices.WESTERN_ZODIAC_CHOICE)
    eastern_zodiac = models.SmallIntegerField(
        editable=False, default=0, choices=single_choices.EASTERN_ZODIAC_CHOICE)

    class Meta:
        index_together = [['user', 'city', 'dob', 'gender', 'pic'],
                          ['city', 'dob', 'gender'], ]

    def __str__(self):
        s = "UserProfile for {0} (#{1})"
        return s.format(self.user.id, self.user.username)

    def save(self, *args, **kwargs):
        if self.dob:
            self.western_zodiac = self.get_western_zodiac()
            self.eastern_zodiac = self.get_eastern_zodiac()
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def language(self):
        return settings.LANGUAGE_CODE[:2]

    @property
    def pic_url_s(self):
        return self.get_pic_url(self.pic_id, 's')

    @property
    def pic_url_m(self):
        return self.get_pic_url(self.pic_id, 'm')

    @property
    def pic_url_x(self):
        return self.get_pic_url(self.pic_id, 'x')

    @property
    def age(self):
        return self.get_age()

    @property
    def crc(self):
        return self.get_crc()

    @property
    def is_online(self):
        return self.get_is_online()

    @property
    def is_idle(self):
        return self.get_is_idle()

    @property
    def is_offline(self):
        return self.get_is_offline()

    @classmethod
    def get_pic_url(cls, pic, size='s'):
        # Try to attach the pic urls here to avoid having to hit the UserPic
        # model simply to display the profile avatar pic.
        # /[MEDIA_URL]/[size]/[int(pic_id/10000)]/[pic_id].jpg

        if isinstance(pic, UserPic):  # Accept both UserPic objs and ints.
            pic_id = pic.id
        elif isinstance(pic, int):
            pic_id = pic
        else:  # If its None or something, then return a "has no picture" image.
            return os.path.join(settings.STATIC_URL,
                                'img/404-userpic-{}.jpg'.format(size))
        sub = str(int(floor(pic_id / 10000)))
        base = settings.MEDIA_URL.rstrip('/')
        return '{}/{}/{}/{}.jpg'.format(base, size, sub, pic_id)

    def get_absolute_url(self):
        # Return the URL path of the profile.
        return reverse('user_profile', args=[self.user.username])

    @classmethod
    def get_crc_list(cls, city_id_list):
        li = AltName.objects.filter(
            geoname_id__in=city_id_list, type=3, is_main=True,
            language=(get_language() or settings.LANGUAGE_CODE)[:2]
        ).values('geoname_id', 'crc')
        return {a['geoname_id']: a['crc'] for a in li}

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
            return [y[1] for y in a if y[0] == self.gender][0]
        except IndexError:
            return ''

    def get_gender_heshe(self):
        try:
            a = single_choices.GENDER_CHOICE_HESHE
            return [y[1] for y in a if y[0] == self.gender][0]
        except IndexError:
            return ''

    def get_gender_hisher(self):
        try:
            a = single_choices.GENDER_CHOICE_HISHER
            return [y[1] for y in a if y[0] == self.gender][0]
        except IndexError:
            return ''

    # noinspection PyTypeChecker,PyBroadException
    def get_age(self):
        try:
            delta = date.today() - self.dob
            return int(delta.days / 365)
        except:
            return ''

    # noinspection PyBroadException
    def get_western_zodiac(self):
        try:
            mdd = int(self.dob.strftime('%m%d'))
            lim = single_choices.WESTERN_ZODIAC_UPPER_LIMIT
            return [e[1] for e in lim if mdd < e[0]][0]
        except:
            return 0

    # noinspection PyBroadException
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
            return [y[1] for y in a if y[0] == self.western_zodiac][0]
        except IndexError:
            return ''

    def get_eastern_zodiac_symbol(self):
        try:
            a = single_choices.EASTERN_ZODIAC_SYMBOLS
            return [y[1] for y in a if y[0] == self.eastern_zodiac][0]
        except IndexError:
            return ''

    # noinspection PyTypeChecker
    def get_last_active_seconds(self):
        if self.last_active is None:
            # When instantiated a new UserProfile, needs to return something.
            return 0

        dtime = datetime.utcnow().replace(tzinfo=utc)
        return (dtime - self.last_active).total_seconds()

    def get_is_online(self):
        return (self.get_last_active_seconds() <
                settings.ONLINE_SECONDS_SINCE_LAST_ACTIVE)

    def get_is_idle(self):
        y = settings.IDLE_SECONDS_SINCE_LAST_ACTIVE
        return self.get_last_active_seconds() < y and not self.get_is_online()

    def get_is_offline(self):
        return not self.get_is_online() and not self.get_is_idle()

    def get_friends(self):
        """Return list of user objects that are friends (reciprocal friends
        flag) by profile user."""
        f1 = User.objects.filter(has_flagged__receiver=self.user,
                                 has_flagged__confirmed__isnull=False,
                                 has_flagged__flag_type=1)
        f2 = User.objects.filter(was_flagged__sender=self.user,
                                 was_flagged__confirmed__isnull=False,
                                 was_flagged__flag_type=1)
        return (list(f1.prefetch_related('profile')) +
                list(f2.prefetch_related('profile')))


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


# noinspection PyUnusedLocal
@receiver(pre_delete, sender=User)
def delete_profile_for_user(sender, instance=None, **kwargs):
    if instance:
        user_profile = UserProfile.objects.get(user=instance)
        user_profile.delete()
