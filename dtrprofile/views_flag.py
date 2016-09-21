import json
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from django.views.decorators.http import require_http_methods

from dtrprofile.models_flag import USERFLAG_TYPES, UserFlag
from dtrprofile.models_profile import UserProfile
from dtrprofile.models_usermsg import UserMsg


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
