import calendar
import json
from datetime import time as dt_time, datetime, date, timedelta

import pytz as pytz
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Max, CharField, Value
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from dtrprofile.models_flag import UserFlag
from dtrprofile.models_profile import UserProfile
from dtrprofile.models_talk import Talk
from dtrprofile.models_usermsg import UserMsg


per_page = 100


def date_from_isoformat(s):
    y, m, d = [int(x) for x in s[:10].split('-', 2)]
    return date(y, m, d)


def status_messages_heavy_senders(from_date=None, to_date=None, page=1):
    """Count messages-per-user for all-time"""
    page = int(page) or 1
    _first, _last = (page-1) * per_page, page * per_page

    if not from_date:
        from_date = '1970-01-01'
    if not to_date:
        to_date = date.today().isoformat()

    dt_from = datetime.combine(from_date, dt_time(0, 0)).replace(tzinfo=pytz.utc)
    dt_to = datetime.combine(to_date, dt_time(23, 59)).replace(tzinfo=pytz.utc)

    return UserMsg.objects.all()\
        .filter(created__gte=dt_from)\
        .filter(created__lte=dt_to)\
        .values('from_user')\
        .annotate(count=Count('from_user'))\
        .order_by('-count')\
        .values_list('count', 'from_user__username', 'from_user__date_joined',
                     'from_user__last_login')[_first:_last]


def status_messages_recent_senders(page=1):
    page = int(page) or 1
    _first, _last = (page-1) * per_page, page * per_page

    return UserMsg.objects.values('from_user')\
        .annotate(max_created=Max('created'))\
        .annotate(count=Value('-', output_field=CharField()))\
        .order_by('-max_created')\
        .values_list('count', 'from_user__username',
                     'max_created', 'from_user__date_joined')[_first:_last]


@user_passes_test(lambda u: u.is_staff)
def status_messages_user_msgs_json(request):
    """Return latest messages by user for spam review by admin."""
    limit = request.GET.get('limit', 100)
    username = request.GET.get('u', None)
    user = get_object_or_404(User, username=username)
    msgs = list(UserMsg.objects.filter(from_user=user).order_by('-pk').values(
        'to_user__username', 'is_replied', 'created', 'created_ip',
        'text')[:limit])
    return JsonResponse({'msgs': msgs})


@user_passes_test(lambda u: u.is_staff)
def status_messages_userlist_json(request):
    from_date = date_from_isoformat(request.GET.get('from', '1970-01-01'))
    to_date = date_from_isoformat(request.GET.get('to', date.today().isoformat()))
    page = request.GET.get('page', 1)
    q = request.GET.get('q', 'most')

    if q == 'recent':
        data = status_messages_recent_senders(page)
    else:
        # default: 'most'
        data = status_messages_heavy_senders(from_date, to_date, page)

    return JsonResponse({
        'userlist': list(data),
    })


def status_messages(request, template_name="dtrprofile/status_messages.html"):
    return render(request, template_name, {})


def status_page(request, template_name="dtrprofile/status.html"):

    def per_day_for_range_from_model(day_from, day_until, model, field):
        """
        For model, counts items-per-day for a secified date range, with
        field being the date field to look through.
        """
        noon = dt_time(12, 0)  # Set all to noon.
        d1 = datetime.combine(day_from, noon).replace(tzinfo=pytz.utc)
        d2 = datetime.combine(day_until, noon).replace(tzinfo=pytz.utc)
        qs = model.objects.filter(**{field+'__gte': d1, field+'__lte': d2})
        qs = qs.extra({'day': 'date('+field+')'}).values('day')
        qs = qs.annotate(count=Count('pk')).order_by('day')
        return qs

    # def per_day_for_month_from_model(year, month, model, field='created'):
    #     day_from = datetime(year, month, 1)
    #     day_until = datetime(year, month, calendar.monthrange(year, month)[1])
    #     return per_day_for_range_from_model(day_from, day_until, model, field)

    def per_day_for_year_from_model(year, model, field='created'):
        day_from = datetime(year, 1, 1)
        day_until = datetime(year, 12, calendar.monthrange(year, 12)[1])
        return per_day_for_range_from_model(day_from, day_until, model, field)

    def every_in_in_year(year):
        day_from = date(year, 1, 1)
        day_until = date(year, 12, calendar.monthrange(year, 12)[1])
        delta = day_until - day_from
        r = range(delta.days + 1)
        return [[(day_from + timedelta(days=i)).isoformat()] for i in r]

    def append_column_by_day(datali, itemli):
        for y in datali:
            field = 0  # default, if there is no data for this day
            for x in itemli:
                if y[0] == x['day'].isoformat():
                    field = x['count']
            y.append(field)
        return datali

    # noinspection PyTypeChecker
    def get_dailies_aggregated(year):
        header = ['Date']
        datali = every_in_in_year(year)

        header.append('Messages sent')
        itemli = per_day_for_year_from_model(year, UserMsg)
        datali = append_column_by_day(datali, itemli)

        header.append('Talk sent')
        itemli = per_day_for_year_from_model(year, Talk)
        datali = append_column_by_day(datali, itemli)

        header.append('Flags set')
        itemli = per_day_for_year_from_model(year, UserFlag)
        datali = append_column_by_day(datali, itemli)

        return json.dumps([header] + datali)

    # noinspection PyTypeChecker
    def get_dailies_aggregated_2(year):
        header = ['Date']
        datali = every_in_in_year(year)

        header.append('Signups')
        itemli = per_day_for_year_from_model(year, User, 'date_joined')
        datali = append_column_by_day(datali, itemli)

        header.append('Logins')
        itemli = per_day_for_year_from_model(year, User, 'last_login')
        datali = append_column_by_day(datali, itemli)

        header.append('Last active')
        itemli = per_day_for_year_from_model(year, UserProfile, 'last_active')
        datali = append_column_by_day(datali, itemli)

        return json.dumps([header] + datali)

    days_30 = (datetime.utcnow() - timedelta(days=30)).replace(tzinfo=pytz.utc)
    mon_12 = (datetime.utcnow() - timedelta(days=365)).replace(tzinfo=pytz.utc)

    msgs_sent_past_30d = UserMsg.objects.filter(created__gt=days_30).count()
    msgs_sent_past_12m = UserMsg.objects.filter(created__gt=mon_12).count()

    talk_sent_past_30d = Talk.objects.filter(created__gt=days_30).count()
    talk_sent_past_12m = Talk.objects.filter(created__gt=mon_12).count()

    signup_past_30d = User.objects.filter(date_joined__gt=days_30).count()
    signup_past_12m = User.objects.filter(date_joined__gt=mon_12).count()

    login_past_30d = User.objects.filter(last_login__gt=days_30).count()
    login_past_12m = User.objects.filter(last_login__gt=mon_12).count()

    active_past_30d = UserProfile.objects.filter(
        last_active__gt=days_30).count()
    active_past_12m = UserProfile.objects.filter(
        last_active__gt=mon_12).count()

    flags_past_30d = UserFlag.objects.filter(created__gt=days_30).count()
    flags_past_12m = UserFlag.objects.filter(created__gt=mon_12).count()

    ctx = {

        'dailies_aggregated_1': get_dailies_aggregated(2016),
        'dailies_aggregated_2': get_dailies_aggregated_2(2016),

        'msgs_sent_past_30d': msgs_sent_past_30d,
        'msgs_sent_past_30d_avg_day': int(msgs_sent_past_30d / 30),
        'msgs_sent_past_12m': msgs_sent_past_12m,
        'msgs_sent_past_12m_avg_mon': int(msgs_sent_past_12m / 12),
        'msgs_sent_past_12m_avg_day': int(msgs_sent_past_12m / 365),

        'talk_sent_past_30d': talk_sent_past_30d,
        'talk_sent_past_30d_avg_day': int(talk_sent_past_30d / 30),
        'talk_sent_past_12m': talk_sent_past_12m,
        'talk_sent_past_12m_avg_mon': int(talk_sent_past_12m / 12),
        'talk_sent_past_12m_avg_day': int(talk_sent_past_12m / 365),

        'signup_past_30d': signup_past_30d,
        'signup_past_30d_avg_day': int(signup_past_30d / 30),
        'signup_past_12m': signup_past_12m,
        'signup_past_12m_avg_mon': int(signup_past_12m / 12),
        'signup_past_12m_avg_day': int(signup_past_12m / 365),

        'login_past_30d': login_past_30d,
        'login_past_30d_avg_day': int(login_past_30d / 30),
        'login_past_12m': login_past_12m,
        'login_past_12m_avg_mon': int(login_past_12m / 12),
        'login_past_12m_avg_day': int(login_past_12m / 365),

        'active_past_30d': active_past_30d,
        'active_past_30d_avg_day': int(active_past_30d / 30),
        'active_past_12m': active_past_12m,
        'active_past_12m_avg_mon': int(active_past_12m / 12),
        'active_past_12m_avg_day': int(active_past_12m / 365),

        'flags_past_30d': flags_past_30d,
        'flags_past_30d_avg_day': int(flags_past_30d / 30),
        'flags_past_12m': flags_past_12m,
        'flags_past_12m_avg_mon': int(flags_past_12m / 12),
        'flags_past_12m_avg_day': int(flags_past_12m / 365),

    }
    return render(request, template_name, ctx)