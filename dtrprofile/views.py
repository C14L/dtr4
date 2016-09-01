# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from dtrprofile.forms import UserEditProfileForm

"""
Manage user profiles, pics, messages between users, and more.

Main app for the project, manages public and private messages and flags
between users, pics and profiles. Return only JSON encoded data, try
not to return any HTML pages.
"""

import json
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, Http404  # 301
from django.http import HttpResponseBadRequest          # 400
from django.http import HttpResponseForbidden           # 403
from django.http import HttpResponseNotFound            # 404
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.utils.timezone import utc
from django.utils.timezone import now as timezone_now
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dtrcity.models import City
from dtrprofile.models import (UserPic, UserMsg, UserFlag,
                               Talk, TalkHashtag, TalkUsername, UserProfile)
from dtrprofile.models import USERFLAG_TYPES
from dtrprofile.serializers import UserMsgSerializer, InboxSerializer
from dtrprofile.utils import get_client_ip


# Homepage view

def homepage(request, template_name="dtrprofile/site_index.es.html"):
    """The homepage view at "/".

    If the user is logged in, simply redirect to the app's startpage.

    Otherwise, serve a HTML page with forms for login and signup, as
    well as some text content describing the purpose of the site, both
    for SEO and for the user.
    """
    # Authenticated user load app
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect(settings.LOGIN_REDIRECT_URL)
    # Anon users get a nice home page.
    return render_to_response(template_name, context=RequestContext(request))


# Private Messages

# noinspection PyMethodMayBeStatic
class UserMsgList(APIView):
    """Private messages between the authuser and one other user.

    To be displayed when the authuser views the other user's profile
    page.
    """

    def can_send_msg(self, sender, receiver):
        """Returns True if sender has permission to message receiver.

        sender User object of message author, most likely request.user
        receiver User object of message receipient.
        """
        # Careful: "receiver" of flag is "sender" of message.
        return not UserFlag.objects.filter(
            receiver=sender, sender=receiver, flag_type=3).exists()

    def send_new_msg_email(self, request, user, msg):
        """Send a 'you have a new message' email.

        request The request context.
        user The receipient of the private message.
        msg The text string of the message.

        Verifies that the receipient has an email address in their
        account and that they have not received a "new message" email
        within a set amount of time.
        """
        # Default minimum time between two notification emails.
        gap_sec = 60 * getattr(settings, 'SEND_EMAIL_TIMEGAP_MINUTES', 60)
        gap_ok = ((not user.profile.last_email) or (timezone_now() -
                  user.profile.last_email).total_seconds() > gap_sec)

        if user.email and gap_ok:
            from_user = request.user
            lg = get_language()[:2].lower()
            fn = 'dtrprofile/email_notify_new_private_message.{}'.format(lg)
            plaintext = get_template('{}.txt'.format(fn))
            # noinspection PyBroadException
            try:
                # optional html version
                htmltext = get_template('{}.html'.format(fn))
            except:
                htmltext = None

            d = Context({'user': user, 'from_user': from_user,
                         'msg': msg, 'site': get_current_site(request)})
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            subject, text_content = plaintext.render(d).split('\n\n', 1)
            html_content = None
            if htmltext:  # optional
                html_content = htmltext.render(d)
            email = EmailMultiAlternatives(subject, text_content,
                                           from_email, [to_email])
            if htmltext:  # optional
                email.attach_alternative(html_content, "text/html")
            email.send()

            # Remember the time when this email was sent.
            user.profile.last_email = timezone_now()
            user.profile.save()

    def fetch_usermsgs(self, receiver, sender,
                       after=None, before=None, count=20):
        """Return a QuerySet of "count" messages between two users.

        If after or before is set, return only messages that were sent
        after/before that timestamp.

        The messages received by receiver are set to "is_read=True"
        automatically.
        """
        usermsgs = UserMsg.objects.filter(
            Q(from_user=receiver, to_user=sender) |
            Q(from_user=sender, to_user=receiver))
        if after:
            usermsgs = usermsgs.filter(created__gt=after)
        if before:
            usermsgs = usermsgs.filter(created__lt=before)
        # This will set all messages received by "to_user" and sent by
        # "from_user" to "is_read=True", because "to_user" as the
        # receipient has seen them now.
        UserMsg.set_is_read(from_user=sender, to_user=receiver)
        return usermsgs.order_by('-pk')[:count]

    @method_decorator(login_required)
    def get(self, request, username):
        usermsgs = self.fetch_usermsgs(
            request.user,
            get_object_or_404(User, username=username),
            request.GET.get('after', None),
            request.GET.get('before', None), 20)
        # TODO: Doesn't load older messages yet.
        serializer = UserMsgSerializer(usermsgs, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def post(self, request, username):
        """Send a private message from request.user to user."""
        after = request.POST.get('after', None)
        user = get_object_or_404(User, username=username)
        # Check if request.user has permission to message user.
        if not self.can_send_msg(request.user, user):
            return HttpResponseBadRequest('Can not send message.')
        # Expected values: text:<message text>
        data = request.data
        data['to_user'] = user.pk
        data['from_user'] = request.user.pk
        data['created'] = timezone_now()
        serializer = UserMsgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Send notification email to receipient.
            self.send_new_msg_email(request, user, data['text'])
            # return ALL posts since last check (after) NOT only this one.
            if after is None:
                # get the last ten or so to make sure we catch up.
                usermsgs = self.fetch_usermsgs(request.user, user, count=10)
            else:
                # return all messages after the last the user received.
                usermsgs = self.fetch_usermsgs(request.user, user, after)
            #
            # TODO: this should return all new messages since "after" but it
            #       doesn't for some reason. 2014-12-19
            #
            serializer = UserMsgSerializer(usermsgs, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Something went wrong in the serializer.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InboxList(APIView):
    """Return lists for unread, inbox, and sent messages.

    List all messages authuser has received (t=recv), has sent (t=sent)
    or all received messages not yet read (t=unread). GET[after] or
    GET[before] may have a timestamp to load only messages "created"
    before or after that time.
    """

    @method_decorator(login_required)
    def get(self, request, t=None):
        count = request.GET.get('count', 20)
        after = request.GET.get('after', None)
        before = request.GET.get('before', None)
        # Build the messages query
        usermsgs = UserMsg.objects.all().order_by('-created')
        # set what box to load
        if t == 'recv':
            usermsgs = usermsgs.filter(to_user=request.user, is_blocked=False)
        elif t == 'unread':
            usermsgs = usermsgs.filter(to_user=request.user,
                                       is_read=False, is_blocked=False)
        elif t == 'sent':
            usermsgs = usermsgs.filter(from_user=request.user)
        else:
            return Response([], status=status.HTTP_404_NOT_FOUND)
        # add time limits, if requested
        if before:
            usermsgs = usermsgs.filter(created__lt=before)
        elif after:
            usermsgs = usermsgs.filter(created__gt=after)
        # and finally serialize and return the list
        serializer = InboxSerializer(usermsgs[:count], many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def post(self, request, t=None):
        """Set all of authuser's received messages to "is_read"."""
        # TODO: use GET['read']==1 GET['replied']==1 here, to mirror the
        # setting for invididual messages below.
        if t == 'allread':
            UserMsg.set_is_read_all(request.user)
            return HttpResponse()
        else:
            return HttpResponseNotFound()


class InboxItem(APIView):
    """To set individual messages manually to is_read or is_replied."""

    @method_decorator(login_required)
    def post(self, request, pk):
        # decode json from body
        body = json.loads(request.body.decode("utf-8"))
        # either "1" or "0" to set or unset status.
        is_read = int(body.get('is_read', -1))
        is_replied = int(body.get('is_replied', -1))
        item = get_object_or_404(UserMsg, pk=pk, to_user=request.user)
        if is_read == 0:
            item.is_read = False
        if is_read == 1:
            item.is_read = True
        if is_replied == 0:
            item.is_replied = False
        if is_replied == 1:
            item.is_replied = True
        item.save()
        return HttpResponse()


# Below are function based views. - -


# - - flags and lists - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@login_required()
@require_http_methods(["GET", "HEAD"])
def profile_flag_list(request, listname):
    """Return a list of users based on their relation to authuser.

    listname: one of the defined list names 'matches', 'like_me',
              'likes', 'viewed_me', 'favorites', 'friends',
              'friend_recv', 'friend_sent', or 'blocked'.

    Find all users that have the requested relation to authuser and
    return a list of basic user data dicts. Not complete User objects!
    """
    after = request.GET.get('after', None)
    flags = None
    data = []
    lists = ['matches', 'like_me', 'likes', 'viewed_me', 'favorites',
             'friends', 'friend_recv', 'friend_sent', 'blocked']
    if listname not in lists:
        return HttpResponseNotFound()

    # two-way lists: difference between "invite" and "mutual".
    if listname == "matches":  # 2=like
        flags = UserFlag.objects.filter(flag_type=2, confirmed__isnull=False)\
                                .filter(Q(receiver=request.user) |
                                        Q(sender=request.user))
    elif listname == "like_me":  # 2=like
        flags = UserFlag.objects.filter(flag_type=2, receiver=request.user,
                                        confirmed__isnull=True)
    elif listname == "likes":  # 2=like
        flags = UserFlag.objects.filter(flag_type=2, sender=request.user,
                                        confirmed__isnull=True)
    if listname == "friends":  # 1=friend
        flags = UserFlag.objects.filter(flag_type=1, confirmed__isnull=False)\
                                .filter(Q(receiver=request.user) |
                                        Q(sender=request.user))
    elif listname == "friend_recv":  # 1=friend
        flags = UserFlag.objects.filter(flag_type=1, receiver=request.user,
                                        confirmed__isnull=True)
    elif listname == "friend_sent":  # 1=friend
        flags = UserFlag.objects.filter(flag_type=1, sender=request.user,
                                        confirmed__isnull=True)

    # one-way lists: not important if "mutual".
    elif listname == "viewed_me":  # 5=viewed
        flags = UserFlag.objects.filter(flag_type=5, receiver=request.user)
    elif listname == "favorites":  # 4=favorite
        flags = UserFlag.objects.filter(flag_type=4, sender=request.user)
    elif listname == "blocked":  # 3=block
        flags = UserFlag.objects.filter(flag_type=3, sender=request.user)
    # blocked users should only ever show up on the "blocked" list, and
    # be not displayed on any others. So, do remove them from any list
    # but the actual blocked list.
    if listname != "blocked":
        # fetch a list of User pk values that were blocked by authuser.
        blocklist = UserFlag.objects.filter(flag_type=3, sender=request.user)
        blocklist = blocklist.values_list('receiver', flat=True)

    # Prefetches now and limits the query by "after" parameter. However, there
    # is still a query to City model for each iteration on flags. Example:
    #
    # SELECT ••• FROM `dtrcity_altname` WHERE (`dtrcity_altname`.`geoname_id` =
    # 3871336 AND `dtrcity_altname`.`type` = 3 AND `dtrcity_altname`.`language`
    # = 'es' AND `dtrcity_altname`.`is_main` = 1)
    #
    # TODO: prefetch related `City` objects for all items in `flags`.

    if after:
        # Limit the matches to those created after the given datetime.
        flags = flags.filter(created__gt=after)

    flags = flags.prefetch_related('sender', 'sender__profile',
                                   'receiver', 'receiver__profile')

    # Fetch all i18n'ed geonames at once and join onto flags instances
    city_id_li = [x.sender.profile.city_id for x in flags] +\
                 [x.receiver.profile.city_id for x in flags]
    geoname_li = UserProfile.get_crc_list(city_id_li)  # {geoname_id: crc}

    for flag in flags:
        # serialize the found flags into a list of basic user dicts, but
        # remove any blocked users.
        if flag.sender == request.user:
            if listname != "blocked" and flag.receiver.pk in blocklist:
                continue
            # The "other" is the user that is not authuser.
            other = flag.receiver
        else:
            if listname != "blocked" and flag.sender.pk in blocklist:
                continue
            # Again, the "other" is the user that is not authuser.
            other = flag.sender

        # Build the user data dict.
        item = {
            'id': other.id,
            'username': other.username,
            'is_staff': other.is_staff,
            'last_active': other.profile.last_active.isoformat(),
            # 'created': other.date_joined.isoformat(),
            'pic': other.profile.pic_id,
            'age': other.profile.age,
            'gender': other.profile.gender,
            'crc': geoname_li.get(other.profile.city_id, ''),
            # 'city': other.profile.city.pk,
            # 'country': other.profile.country.pk,
        }
        if flag.created:
            item['created'] = flag.created.isoformat()
        if flag.confirmed:
            item['confirmed'] = flag.confirmed.isoformat()
        data.append(item)

    if settings.ENABLE_DEBUG_TOOLBAR:
        return HttpResponse('<html><body>DTB: {}</body></html>'.format(data))

    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


@login_required()
@require_http_methods(["POST", "DELETE"])
def profile_flag(request, flag_name, username):
    data = []
    user = get_object_or_404(User, username=username)
    try:
        flag_type, flag_name, two_way_flag = [x for x in USERFLAG_TYPES
                                              if x[1] == flag_name][0]
    except IndexError:
        # The requested flag_name does not exist.
        return HttpResponseNotFound()

    if request.method == 'POST':
        # Check if flag or confirm already exists.
        flag = None

        try:
            # check if authuser already set the flag
            flag = UserFlag.objects.get(flag_type=flag_type,
                                        sender=request.user, receiver=user)
        except UserFlag.DoesNotExist:
            pass

        # If not and this is two-way, check if authuser confirmed a flag
        if flag is None and two_way_flag:
            try:
                flag = UserFlag.objects.get(flag_type=flag_type,
                                            sender=user, receiver=request.user)
            except UserFlag.DoesNotExist:
                pass

        # If no flag exists yet, add a new flag
        if flag is None:
            flag = UserFlag()
            flag.flag_type = flag_type
            flag.sender = request.user
            flag.receiver = user
            flag.created = datetime.utcnow().replace(tzinfo=utc)
            flag.save()

        # or for two-way, if there was an unconfirmed flag, confirm it
        elif flag is not None and flag.sender == user and not flag.confirmed:
            flag.confirmed = datetime.utcnow().replace(tzinfo=utc)
            flag.save()

        if flag_name == 'block':
            # EVIL SHORTCUT!!! if "block" flag is set, set "UserMsg.is_blocked"
            # on all msgs that have authuser as "to_user", user as "from_user".
            # TODO: Remove this and lookup the "blocked" status between users
            # each time messages are loaded.
            UserMsg.objects.filter(to_user=request.user,
                                   from_user=user).update(is_blocked=True)

    elif request.method == 'DELETE':

        flag = UserFlag.get_flag(flag_name, request.user, user)
        # done = False

        if two_way_flag:
            if flag.receiver == request.user and flag.confirmed:
                flag.confirmed = None
                flag.save()

            elif flag.sender == request.user:
                old_confirmed = flag.confirmed
                flag.delete()

                if flag.confirmed:
                    # if was confirmed, so we need to remove this flag, and set
                    # a new flag with the previous receiver as sender.
                    UserFlag.objects.create(
                        sender=user, receiver=request.user,
                        flag_type=flag_type, created=old_confirmed)
        else:
            # for a one-way, just delete it.
            flag.delete()

        if flag_name == 'block':
            # EVIL SHORTCUT --> if "block" flag is removed, also remove all
            # "UserMsg.is_blocked" on msgs that have authuser as "to_user" and
            # user as "from_user".
            UserMsg.objects.filter(to_user=request.user,
                                   from_user=user).update(is_blocked=False)

    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


# - - pictures - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@login_required()
@csrf_exempt  # TODO: FIXME!
@require_http_methods(["POST"])
def profile_pics_list(request):
    """Create user uploaded photos."""
    if request.method == 'POST':
        if len(request.FILES) != 1:
            return HttpResponseBadRequest('upload one image file')

        # Create a DB row first, then use the ID as filename, save the
        # image file, and update the DB row with the image object.
        pic = UserPic.objects.create(user=request.user,
                                     created_ip=get_client_ip(request))

        pic_filename = '{}.jpg'.format(pic.id)
        pic.pic = request.FILES['file']
        pic.pic.save(pic_filename, request.FILES['file'])
        pic.save()

        # If this is the user's first pic, then set as profile avatar,
        # and attach the avatar to the existing userprofile object.
        if request.user.profile.pic is None:
            request.user.profile.pic = pic
            request.user.profile.save()

        # Return only the new pic's id.
        data = {'pic': pic.id}
        return HttpResponse(json.dumps(data),
                            {'content_type': 'application/json'})

"""
def SOMETHING_ELSE_profile_pics_list(request):
    body = json.loads(request.body.decode("utf-8")) # decode json from body

    if body.get('image', None):
        image_b64 = body.get('image')
        print('image_b64 type, length: {0}, {1}'
              ''.format(len(image_b64), type(image_b64)))

        begin_raw_data = image_b64.find(",") + 1
        print('begin_raw_data at: {0}'.format(begin_raw_data))

        image_raw_base64 = image_b64[begin_raw_data:]
        print('image_raw_base64 type, length: {0}, {1}'\
              ''.format(len(image_raw_base64), type(image_raw_base64)))

        image_data = base64.urlsafe_b64decode(
            image_raw_base64 + ('=' * (4 - len(image_raw_base64) % 4)))
        print('image_data type: {0}'.format(type(image_data)))

        tmp_filename = '/tmp/' + str(uuid.uuid1())
        print('tmp_filename: {0}'.format(tmp_filename))

        with open(tmp_filename + '.png', 'wb') as fh:
            fh.write(image_data)
            print('PNG file written.')

        with Image.open(tmp_filename + '.png', 'r') as im:
            print('PNG file opened as image.')
            im.save(tmp_filename + '.jpg', 'JPEG', quality=85, optimize=True)
            print('JPEG file written.')

        pic = UserPic.objects.create(user=request.user)  # create db entry
        print('UserPic object created')                  # to get new id
        pic_filename = '{}.jpg'.format(pic.id)
        print('pic_filename: {}'.format(pic_filename))

        pic.created_ip = get_client_ip(request)
        pic.pic = tmp_filename + '.jpg'

        print('Now saving UserPic object...')
        pic.pic.save(pic_filename, tmp_filename + '.jpg')
        print('Saving file with pic.pic.save() finished.')
        pic.save()
        print('Saving UserPic object with pic.save() finished.')

        data = { 'pic': pic.id } # Return only the new pic's id.
        print('All done. Send respond data.')
        return HttpResponse(json.dumps(data),
                            {'content_type':'application/json'})
"""


@login_required()
@require_http_methods(["DELETE"])
def profile_pics_item(request, pic_id):
    """Delete user uploaded photos."""
    data = []
    pic = UserPic.objects.get(pk=pic_id)

    if pic.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden('You can only delete your own photos.')

    pic.pic.delete()
    pic.delete()

    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


# - - profile - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# noinspection PyUnusedLocal
@login_required()
@require_http_methods(["GET", "HEAD", "POST", "DELETE"])
def profile_api_view(request, q, use):
    """Return a JSON view with extensive data on one user.

    Either by the user's pk or the username.
    """
    if use == 'username':
        user = get_object_or_404(User, username=q)
    elif use == 'user_id':
        user = get_object_or_404(User, pk=q)
    elif use == 'authuser':
        user = request.user
    else:
        raise Http404

    if request.method == "POST":
        # get data payload
        if request.body:
            jsonstr = request.body.decode("utf-8")

            if type(jsonstr) != unicode:
                jsonstr = jsonstr.decode('utf-8')   # bytes -> Unicode

            body = json.loads(jsonstr)
        else:
            body = {}

        if body.get('pic', None) is not None:
            # Set "pic" as authuser's main profile picture.
            try:
                pic = UserPic.objects.get(pk=body.get('pic', None))
                request.user.profile.pic = pic
            except UserPic.DoesNotExist:
                pass

        if body.get('city', None) is not None:
            try:
                city = City.objects.get(pk=body.get('city', None))
                request.user.profile.city = city
                request.user.profile.country = city.country
                request.user.profile.lat = city.lat
                request.user.profile.lng = city.lng
            except City.DoesNotExist:
                # the user selected no city
                request.user.profile.city = None
                request.user.profile.country = None
                # Do not accept country-only data!
                # try:
                #    # but maybe we have a country?
                #    country = Country.objects.get(pk=body.get('country', None))
                #    request.user.profile.country = country
                # except country.DoesNotExist:
                #    # nope, then set to "unknown" too
                #    request.user.profile.country = None

        if body.get('lat', None) is not None \
                and body.get('lng', None) is not None:
            # maybe overwrite with more precise lat/lng given?
            request.user.profile.lat = body.get('lat', None)
            request.user.profile.lng = body.get('lng', None)

        if body.get('new_password_1', None) is not None\
                or body.get('new_password_2', None) is not None:
            pw_1 = body.get('new_password_1', '')
            pw_2 = body.get('new_password_2', None)
            if not request.user.check_password(body.get('old_password', None)):
                return HttpResponseBadRequest('old_password')
            if len(pw_1) < 6 or pw_1 != pw_2:
                return HttpResponseBadRequest('new_password_1')
            request.user.set_password(pw_1)
            request.user.save()

        if body.get('email', None) is not None:
            if not request.user.check_password(body.get('old_password', None)):
                return HttpResponseBadRequest('old_password')
            request.user.email = body.get('email')
            request.user.save()

        # all the other standard data fields on "User.profile"
        fields = ['aboutme', 'aboutbooks', 'aboutmovies', 'aboutmusic',
                  'aboutarts', 'abouttravel', 'aboutfood', 'aboutquotes',
                  'aboutsports', 'drink', 'diet', 'figure', 'fitness', 'pot',
                  'education', 'eyecolor', 'gender', 'lookingfor',
                  'has_children', 'height', 'haircolor', 'income', 'jobfield',
                  'longest_relationship', 'looks', 'relationship_status',
                  'religion', 'religiosity', 'smoke', 'spirituality',
                  'sports', 'style', 'want_children', 'weight',
                  'would_relocate', ]
        for field in fields:
            field_value = body.get(field,  None)
            if field_value is not None:
                setattr(request.user.profile, field, field_value)
        # Set "dob" manually, to catch cases were it is "" empty.
        dob = body.get('dob', '')
        if dob:
            # Verify that dob is well formated
            re_dob = re.compile(r'^(19|20)[0-9][0-9]-[01][0-9]-[0123][0-9]$')
            if re_dob.match(dob):
                request.user.profile.dob = dob
            else:
                request.user.profile.dob = None
        # If style contained some css, then activate it.
        if body.get('style', None) is not None:
            request.user.profile.style_active = body.get('style_active', True)

        # all done, save user
        request.user.profile.save()
        return HttpResponse()  # 200

    if request.method == "DELETE":
        # delete user's profile. Either user's own profile or authuser is_staff
        # and deletes another user's profile.
        if request.user.is_staff:
            ownprofile = False
        elif request.user.id == user.id:
            ownprofile = True
        else:
            return HttpResponseForbidden()

        # Deleted accounts should be completely removed.

        # Text content from all public posts should be replaced by a message
        # that the user account was deleted, user field must be set to None.
        Talk.objects.filter(user=user).update(text='')

        # Text content from all private messages should be preserved, if the
        # user deleted their own account. If the account was removed by staff,
        # then the content should be removed as well (to remove spam)
        # if ownprofile:
        #    UserMsg.objects.filter(from_user=user).update(from_user=None)
        #    Should happen automatically because models.SET_NULL in model def.
        # else:
        #    UserMsg.objects.filter(
        #        from_user=user).update(text='', from_user=None)

        # For some reason I get IntegrityError when trying to set them to NULL
        # so instead just delete all messages send or received by the user.
        # That's BAD UX becasue the other user's "private" inbox is affected
        # and they will feel loss-of-control, but no time now to figure out why
        # the DB contrains don't work as expected...
        UserMsg.objects.filter(from_user=user).delete()
        UserMsg.objects.filter(to_user=user).delete()

        # Preserve all messges sent to the user, but remove association.
        # Should happen automatically because models.SET_NULL in model def.
        # UserMsg.objects.filter(to_user=user).update(to_user=None)

        # All flags on the account should be removed, as well as the related
        # Profile object. The cascading should happen automatically when
        # deleting the User object.
        user.delete()

        # Confirm
        return HttpResponse()  # 200

    if request.method == "GET":
        flags = {}
        if user != request.user:
            # translate the flags into profileuser API flields
            for f in UserFlag.get_one_way_flags(request.user, user):
                name = [x[1] for x in USERFLAG_TYPES if x[0] == f.flag_type][0]
                if f.sender == request.user:
                    flags[name] = f.created.isoformat()
                elif f.sender == user:
                    flags[name + '_received'] = f.created.isoformat()

            for f in UserFlag.get_two_way_flags(request.user, user):
                name = [x[1] for x in USERFLAG_TYPES if x[0] == f.flag_type][0]
                if f.sender == request.user:
                    flags[name] = f.created.isoformat()
                    if f.confirmed is not None:
                        flags[name + '_received'] = f.confirmed.isoformat()
                elif f.sender == user:
                    flags[name + '_received'] = f.created.isoformat()
                    if f.confirmed:
                        flags[name] = f.confirmed.isoformat()

            # count the view, this is not authuser looking at their own profile
            user.profile.views_counter += 1  # no F('views_counter') + 1
            user.profile.save(update_fields=['views_counter'])

        data = {
            "flags": flags,
            # META
            "id": user.pk,
            "is_staff": user.is_staff,
            "last_modified": user.profile.last_modified.isoformat(),
            "last_active": user.profile.last_active.isoformat(),
            "created": user.date_joined.isoformat(),
            "last_login": user.last_login.isoformat(),
            # PNASL
            "pic": user.profile.pic_id,
            "pics": [x.pk for x in user.pics.all().order_by('-pk')],
            "username": user.username,
            "age": user.profile.age,
            "gender": user.profile.gender,
            "city": user.profile.city_id,
            "country": user.profile.country_id,
            "lat": user.profile.lat,
            "lng": user.profile.lng,
            # SETTINGS
            "language": user.profile.language,
            "style_active": user.profile.style_active,
            "style": user.profile.style,
            # COUTNER
            "friend_open_invites_recv_counter":
                user.profile.friend_open_invites_recv_counter,
            "friend_mutual_confirmed_counter":
                user.profile.friend_mutual_confirmed_counter,
            "match_open_invites_recv_counter":
                user.profile.match_open_invites_recv_counter,
            "match_mutual_confirmed_counter":
                user.profile.match_mutual_confirmed_counter,
            "mail_recv_counter": user.profile.mail_recv_counter,
            "mail_sent_counter": user.profile.mail_sent_counter,
            "mail_unread_counter": user.profile.mail_unread_counter,
            "views_counter": user.profile.views_counter,
            # BLAH
            "aboutme": user.profile.aboutme,
            "aboutbooks": user.profile.aboutbooks,
            "aboutmovies": user.profile.aboutmovies,
            "aboutmusic": user.profile.aboutmusic,
            "aboutarts": user.profile.aboutarts,
            "abouttravel": user.profile.abouttravel,
            "aboutfood": user.profile.aboutfood,
            "aboutquotes": user.profile.aboutquotes,
            "aboutsports": user.profile.aboutsports,
            # STUFF
            "lookingfor": user.profile.lookingfor,
            "height": user.profile.height,
            "weight": user.profile.weight,
            "eyecolor": user.profile.eyecolor,
            "haircolor": user.profile.haircolor,
            "relationship_status": user.profile.relationship_status,
            "has_children": user.profile.has_children,
            "want_children": user.profile.want_children,
            "would_relocate": user.profile.would_relocate,
            "smoke": user.profile.smoke,
            "pot": user.profile.pot,
            "drink": user.profile.drink,
            "longest_relationship": user.profile.longest_relationship,
            "looks": user.profile.looks,
            "figure": user.profile.figure,
            "fitness": user.profile.fitness,
            "education": user.profile.education,
            "diet": user.profile.diet,
            "sports": user.profile.sports,
            "religion": user.profile.religion,
            "religiosity": user.profile.religiosity,
            "spirituality": user.profile.spirituality,
            "jobfield": user.profile.jobfield,
            "income": user.profile.income,
            "western_zodiac": user.profile.western_zodiac,
            "eastern_zodiac": user.profile.eastern_zodiac,
        }
        try:
            data['crc'] = user.profile.crc
        except AttributeError:
            data['crc'] = ''
        # attach a list of basic user data of profileuser's friends
        data['friends'] = []
        # Fetch all i18n'ed geonames at once and join onto user.profile instance
        friends_li = user.profile.get_friends()  # ret User instances, ugh!
        friends_city_id_li = [x.profile.city_id for x in friends_li]
        friends_city_li = UserProfile.get_crc_list(friends_city_id_li)
        for x in user.profile.get_friends():
            data['friends'].append({
                    'id': x.id,
                    'username': x.username,
                    'pic': x.profile.pic_id or 0,
                    'age': x.profile.age,
                    'gender': x.profile.gender,
                    'crc': friends_city_li.get(x.profile.city_id, ''),
                })
        # add some extras, depending if authuser is looking at his own
        # profile, of looking at somebody else's profile page
        if user == request.user:
            # authuser can see (and edit) their own profile birthdate
            # noinspection PyBroadException
            try:
                data['dob'] = user.profile.dob.isoformat()
            except:
                data['dob'] = ''
            # tell authuser how many unread mail she has
            data['mail_unread_counter'] = UserMsg.objects.filter(
                is_read=False, to_user=request.user, is_blocked=False).count()
        else:
            # if this is not authuser looking at his own profile, then add the
            # date of the last time profileuser looked at authuser's  profile.
            try:
                data["last_viewed"] = UserFlag.last_viewed(
                    user, request.user).isoformat()
            except AttributeError:
                data['last_viewed'] = 0
            # also, remember this profile view in UserFlags
            flag, created = UserFlag.objects.get_or_create(
                flag_type=5, sender=request.user, receiver=user)
            flag.created = datetime.utcnow().replace(tzinfo=utc)
            flag.save()

        if settings.ENABLE_DEBUG_TOOLBAR:
            return HttpResponse('<html><body>{}</body></html>'.format(data))

        return HttpResponse(json.dumps(data),
                            {'content_type': 'application/json'})


# - - search - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SearchAPIView(View):

    @method_decorator(login_required)
    def get(self, request):
        json_header = {'content_type': 'application/json'}

        page_size = int(request.GET.get('page_size', 20))
        page = int(request.GET.get('page', 1))
        gender = int(request.GET.get('gender', 1))
        # list of usernames to exclude (e.g. profileuser's)
        exclude = request.GET.get('exclude', [])

        # Get the limits for the dob.
        minage = int(request.GET.get('minage', 18))
        maxage = int(request.GET.get('maxage', 99))
        now = datetime.utcnow()
        born_after = now - relativedelta(years=maxage)
        born_before = now - relativedelta(years=minage)

        # get authuser's blocked users
        blocked_qs = UserFlag.objects.filter(sender=request.user,
                                             flag_type=3).values('receiver')
        # set start item for pagination
        last = page * page_size
        first = last - page_size

        # Get a list of cities that are within "dist" distance from "city".
        # noinspection PyBroadException
        try:
            dist = int(request.GET.get('dist', 100))
            city_id = int(request.GET.get('city', request.user.profile.city_id))
            city = City.objects.get(pk=city_id)
            cities = City.get_cities_around_city(city, dist)
        except:
            # If anything goes wrong on the way, return an empty result [].
            # - User may not be logged in
            # - User may not have set their own city and no search city is given
            # - City pk does not exist. ..etc
            return HttpResponse(json.dumps([]), json_header)

        userlist = User.objects\
            .prefetch_related('profile')\
            .filter(is_active=True)\
            .filter(profile__pic__isnull=False)\
            .filter(profile__country__isnull=False)\
            .filter(profile__city__in=cities)\
            .filter(profile__gender=gender)\
            .filter(profile__dob__gt=born_after)\
            .filter(profile__dob__lt=born_before)\
            .exclude(pk=request.user.pk)\
            .exclude(username__in=exclude)\
            .exclude(pk__in=blocked_qs)\
            .order_by('-profile__last_active')[first:last]
        data = []

        # Fetch all i18n'ed geonames at once and join onto user.profile instance
        geonames_li = [x.profile.city_id for x in userlist]
        geonames_li = UserProfile.get_crc_list(geonames_li)

        for user in userlist:
            item = {
                'id': user.pk,
                'last_active': user.profile.last_active.isoformat(),
                'created': user.date_joined.isoformat(),
                'username': user.username,
                'age': user.profile.age,
                'gender': user.profile.gender,
                'pic': user.profile.pic_id,
                'city': user.profile.city_id,
                'country': user.profile.country_id,
                'crc': geonames_li.get(user.profile.city_id, ''),
            }
            data.append(item)

        if settings.ENABLE_DEBUG_TOOLBAR:
            return HttpResponse('<html><body>{}</body></html>'.format(data))

        return HttpResponse(json.dumps(data), json_header)


# - - Others - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@login_required
def edit_profile(req):
    # Basics like PASL
    if req.method == "POST":
        form = UserEditProfileForm(req.POST)

        if form.is_valid():
            req.user.profile.dob = form.cleaned_data['dob']
            req.user.profile.gender = form.cleaned_data['gender']
            # req.user.profile.country = form.cleaned_data['country']
            # req.user.profile.city = form.cleaned_data['city']
            req.user.profile.last_modified = datetime.utcnow()\
                                                     .replace(tzinfo=utc)
            req.user.profile.save()
            return HttpResponse()
    else:
        form = UserEditProfileForm({
            'dob': req.user.profile.dob,
            'gender': req.user.profile.gender,
            # 'country': req.user.profile.country,
            # 'city': req.user.profile.city,
        })

    return HttpResponse(form.as_ul())


# - - Talk - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# GET /api/v1/talk/new.json?after=datetime (or ?before=datetime)
# POST /api/v1/talk/new.json
# GET /api/v1/talk/day/<date>.json
# GET /api/v1/talk/tag/<hashtag>.json
# GET /api/v1/talk/user/<username>.json
# GET /api/v1/talk/item/<talk.id>.json
# DELETE /api/v1/talk/item/<talk.id>.json

def talk_fetch_posts(request, after=None, before=None, count=None, group='all'):
    if count is None:
        count = settings.DTR_TALK_PAGE_SIZE

    # Create the inicial posts object with all posts.
    posts = Talk.objects.filter(is_blocked=False,
                                user__isnull=False).order_by('-created')

    # TODO: Add prefetch for "user" field.

    # Limit posts list by before or after a certain date.
    if before:
        posts = posts.filter(created__lt=before)
    elif after:
        posts = posts.filter(created__gt=after)

    # Limit post to a certain group, one of 'all', 'matches', 'friends'.
    # The option 'own' returns only the user's own posts and is handled
    # elsewhere.
    if group == 'all':
        # No fitering, fetch all as above.
        pass
    elif group == 'matches' and request.user.is_authenticated():
        # Find matches of authuser and only fetch their posts and the authuser's
        # own posts.
        matches_1 = UserFlag.objects.filter(confirmed__isnull=False)\
                                    .filter(flag_type=2)\
                                    .filter(receiver=request.user)\
                                    .values('sender')
        matches_2 = UserFlag.objects.filter(confirmed__isnull=False)\
                                    .filter(flag_type=2)\
                                    .filter(sender=request.user)\
                                    .values('receiver')
        posts = posts.filter(Q(user__in=matches_1) | Q(user__in=matches_2) |
                             Q(user=request.user))
    elif group == 'friends' and request.user.is_authenticated():
        # Find friends of authuser and only fetch their posts and the authuser's
        # own posts.
        friends_1 = UserFlag.objects.filter(confirmed__isnull=False)\
                                    .filter(flag_type=1)\
                                    .filter(receiver=request.user)\
                                    .values('sender')
        friends_2 = UserFlag.objects.filter(confirmed__isnull=False)\
                                    .filter(flag_type=1)\
                                    .filter(sender=request.user)\
                                    .values('receiver')
        posts = posts.filter(Q(user__in=friends_1) | Q(user__in=friends_2) |
                             Q(user=request.user))
    return posts[:count]


def talk_posts_to_dict(request, posts):
    """
    Receives list of Talk objects and converts them into a list of dicts.
    """
    posts = list(posts)
    blocked = []
    # Add "block" flag to each post, if post user was blocked by authuser.
    # For posts written by users that were blocked by authuser: do not remove
    # the posts here. just add a "block" flag to them, and then hide them on
    # the client side, only show a greyed out "blocked" insteat, so authuser
    # has information that there is a post that is not shown, because others
    # may talk about or reference that post.
    if request.user.is_authenticated():
        blocked = UserFlag.objects.filter(flag_type=3)\
                                  .filter(sender=request.user)\
                                  .values_list('receiver', flat=True)
    for i in range(0, len(posts)):
        posts[i] = talk_post_to_dict(posts[i])
        posts[i]['block'] = posts[i]['user']['id'] in blocked
    return posts


def talk_post_to_dict(post):
    try:
        ret = {
            'id': post.id,
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'pic': post.user.profile.pic_id,
                'age': post.user.profile.age,
                'gender': post.user.profile.gender,
                'crc': post.user.profile.crc,
            },
            'created': post.created.isoformat(),
            'child_counter': post.child_counter,
            'views_counter': post.views_counter,
            'text': post.text,
        }
    except AttributeError:
        ret = {
            'id': post.id,
            'user': {
                'id': 0,
                'username': '---',
                'pic': '/static/placeholder.jpg',
                'age': '',
                'gender': '',
                'crc': '',
            },
            'created': post.created.isoformat(),
            'child_counter': post.child_counter,
            'views_counter': post.views_counter,
            'text': post.text,
        }

    return ret


@login_required
@require_http_methods(['PUT', 'GET', 'HEAD', 'DELETE'])
def talk_post(request, post_id):
    """An individual post: delete, update, or retreive."""
    data = []
    post = get_object_or_404(Talk, pk=post_id)

    if request.method in ['GET', 'HEAD']:
        data = talk_post_to_dict(post)
    elif request.method == 'PUT':
        # Updateing a post not implemented.
        return HttpResponseBadRequest('Not implemented.')
    elif request.method == 'DELETE':
        # User can only delete their own posts, except staff who can delete any.
        if post.user != request.user and not request.user.is_staff:
            HttpResponseForbidden('You can only delete your own posts.')
        post.delete()
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


@require_http_methods(['POST', 'GET', 'HEAD'])
def talk_list(request, group='all'):
    """
    GET returns a list of "count" posts, newest first.
    POST receives data of a new post and saves it and returns the new post.
    """
    if group not in ['all', 'matches', 'friends', 'own']:
        return HttpResponseBadRequest()

    if request.method == 'GET':
        group = request.GET.get('group', None)
        after = request.GET.get('after', None)
        before = request.GET.get('before', None)
        count = request.GET.get('count', settings.DTR_TALK_PAGE_SIZE)
        data = talk_fetch_posts(request, after, before, count, group)
        data = talk_posts_to_dict(request, data)
        return HttpResponse(json.dumps(data),
                            {'content_type': 'application/json'})

    elif request.method == 'POST':
        # Only authenticated user may post content.
        if not request.user.is_authenticated():
            url = '{}?next={}'.format(settings.LOGIN_URL, request.path)
            return redirect(url)

        # Decode json from body
        body = json.loads(request.body.decode("utf-8"))
        text = body.get('text', None)
        parent = body.get('parent', None)

        if not text:
            return HttpResponseBadRequest('no nothing')
        if parent:
            try:
                parent = Talk.objects.get(pk=parent)
            except Talk.DoesNotExist:
                parent = None

        # Find any hashtags or usernames mentioned in the post.
        hashtags = set(re.findall(r'#\w{2,50}', text))
        usernames = set(re.findall(r'@\w{3,30}', text))

        # Create the post object.
        post = Talk()
        post.text = text
        post.user = request.user
        post.parent = parent
        post.created = datetime.utcnow().replace(tzinfo=utc)
        post.hashtag_counter = len(hashtags)
        post.username_counter = len(usernames)
        post.save()

        # Write hashtags to TalkHashtag
        for row in hashtags:
            TalkHashtag.objects.create(tag=row.lstrip('#'), talk=post)

        # Write usernames (user objects) to TalkUsername
        usernames = [x.lstrip('@') for x in usernames]
        users = User.objects.filter(username__in=usernames)  # , is_active=True)
        for user in users:
            TalkUsername.objects.create(user=user, talk=post)

        # Return the newly created post object.
        # noinspection PyTypeChecker
        return HttpResponse(json.dumps(talk_post_to_dict(post)),
                            {'content_type': 'application/json'})


@require_http_methods(['GET', 'HEAD'])
def talk_hashtag(request, hashtag):
    """returns a list of posts that are tagged with the hashtag hashtag."""
    after = request.GET.get('after', None)
    before = request.GET.get('before', None)
    count = request.GET.get('count', settings.DTR_TALK_PAGE_SIZE)
    posts = Talk.objects.filter(hashtag__tag__iexact=hashtag).order_by('-pk')
    if after:
        posts = posts.filter(created__gt=after)
    if before:
        posts = posts.filter(created__lt=before)
    data = talk_posts_to_dict(request, posts[:count])
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


@require_http_methods(['GET', 'HEAD'])
def talk_username(request, username):
    """returns a list of posts that mention user "username"."""
    after = request.GET.get('after', None)
    before = request.GET.get('before', None)
    count = request.GET.get('count', settings.DTR_TALK_PAGE_SIZE)
    user = get_object_or_404(User, username__iexact=username)
    posts = Talk.objects.filter(Q(mentions__user=user) |
                                Q(user=user)).order_by('-pk')
    if after:
        posts = posts.filter(created__gt=after)
    if before:
        posts = posts.filter(created__lt=before)
    data = talk_posts_to_dict(request, posts[:count])
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


@require_http_methods(['GET', 'HEAD'])
def talk_popular_tags(request):
    """
    returns a list with the "count" most popular tags within the past "sample"
    tags posted.

    TODO: The "sample" part doesn't work well with MySQL. Change it to grouped
    by date, so that we get "the most popular tag in the last week" or "in the
    past 24 hours" etc.
    """
    count = request.GET.get('count', 20)
    # sample = request.GET.get('sample', 1000)
    tags = TalkHashtag.objects.values('tag').annotate(count=Count('tag'))
    data = [x['tag'] for x in tags.order_by('-count')[:count]]
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


@require_http_methods(['GET', 'HEAD'])
def talk_popular_users(request):
    """
    returns a list with the "count" most popular (most often @mentioned) users
    within the past "sample" users posted.

    TODO: The "sample" part doesn't work well with MySQL. Change it to grouped
    by date, so that we get "the most popular tag in the last week" or "in the
    past 24 hours" etc.
    """
    count = request.GET.get('count', 20)
    # sample = request.GET.get('sample', 1000)
    users = TalkUsername.objects.values('user__username').annotate(
        count=Count('user')).order_by('-count')[:count]
    data = [x['user__username'] for x in users]
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@login_required
@require_http_methods(['GET'])
def pictures_list(request):
    """
    Return a list of most recent user uploaded pictures items. Each item is a
    dict with the fields: id, username, created

    Optionally params: count - number of items to return, between 1 and 500.
                       below_id - only return pics with IDs smaller than this.
    """
    data = []
    count = int(request.GET.get('count', 50))
    below_id = int(request.GET.get('below_id', 0))
    if not count or count < 1 or count > 500:
        count = 50
    pics = UserPic.objects.all().order_by('-created')\
                                .select_related('user__username')
    if below_id:
        pics = pics.filter(id__lt=below_id)
    for pic in pics[:count]:
        data.append({'id': pic.id,
                     'username': pic.user.username,
                     'created': pic.created.isoformat()})
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})
