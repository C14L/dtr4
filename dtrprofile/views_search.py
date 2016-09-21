import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from dtrcity.models import City
from dtrprofile.models_flag import UserFlag
from dtrprofile.models_profile import UserProfile


class SearchAPIView(View):

    @method_decorator(login_required)
    def get(self, request):
        json_header = {'content_type': 'application/json'}

        page_size = int(request.GET.get('page_size', 20))
        page = int(request.GET.get('page', 1))
        page = 1 if page < 1 else page
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


