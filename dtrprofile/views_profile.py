import json
from datetime import datetime

import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse, \
    HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from dtrcity.models import City
from dtrprofile.forms import UserEditProfileForm
from dtrprofile.models_flag import USERFLAG_TYPES, UserFlag
from dtrprofile.models_profile import UserPic, UserProfile
from dtrprofile.models_talk import Talk
from dtrprofile.models_usermsg import UserMsg
from dtrprofile.utils import get_client_ip


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

            if type(jsonstr) != str:
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
            # noinspection PyUnusedLocal
            ownprofile = False
        elif request.user.id == user.id:
            # noinspection PyUnusedLocal
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