import os
from django.conf import settings
from django.conf.urls import include, url, i18n
from django.contrib import admin
from django.contrib.auth.views import logout as logout_view
from django.http import HttpResponse

import dtrprofile.views_flag
import dtrprofile.views_inbox
import dtrprofile.views_profile
import dtrprofile.views_search
import dtrprofile.views_status
import dtrprofile.views_talk
import dtrprofile.views_usermsg
from dtrcity import views as city_views
from dtrprofile import views as profile_views
from dtrseo import views as seo_views

# Define routes
urlpatterns = [

    # - - - HTML pages - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Django's for admin and to change user language
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include(i18n)),

    # First remove extra do-you-really-want-to-log-out step upon logging
    # out, then include all-auth URLs.
    url(r'^accounts/logout/$', logout_view,
        {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^accounts/', include('allauth.urls')),

    # Homepage, that redirects either to login age or to ng app.
    url(r'^$',
        profile_views.homepage, name='home'),
    url(r'^status/?$',
        dtrprofile.views_status.status_page, name='status'),
    url(r'^status/messages/?$',
        dtrprofile.views_status.status_messages, name='status_messages'),
    url(r'^status/messages/detail/?$',
        dtrprofile.views_status.status_messages_user_msgs_json),
    url(r'^status/messages/userlist/?$',
        dtrprofile.views_status.status_messages_userlist_json),

    # - - - JSON API endpoints - - - - - - - - - - - - - - - - - - - - - - - -

    # Pictures

    # GET a list all uploaded pics (for mods only).
    url(r'^api/v1/pics/all.json$', profile_views.pictures_list),

    # Flag

    # GET a list of flagged users
    url(r'^api/v1/lists/(?P<listname>[a-zA-Z0-9_-]{2,50}).json$',
        dtrprofile.views_flag.profile_flag_list),
    # POST or DELETE a flag on a user.
    url(r'^api/v1/flag/(?P<flag_name>\w{1,20})/'
        r'(?P<username>[a-zA-Z0-9_-]{3,30}).json$',
        dtrprofile.views_flag.profile_flag),

    # Talk

    url(r'^api/v1/talk/list.json$',
        dtrprofile.views_talk.talk_list),
    url(r'^api/v1/talk/post/(?P<post_id>\d{1,11}).json$',
        dtrprofile.views_talk.talk_post),
    url(r'^api/v1/talk/topic/(?P<hashtag>\w{2,50}).json$',
        dtrprofile.views_talk.talk_hashtag),
    url(r'^api/v1/talk/people/(?P<username>[a-zA-Z0-9_-]{3,30}).json$',
        dtrprofile.views_talk.talk_username),
    url(r'^api/v1/talk/popular-tags.json$',
        dtrprofile.views_talk.talk_popular_tags),
    url(r'^api/v1/talk/popular-users.json$',
        dtrprofile.views_talk.talk_popular_users),

    # Profile

    url(r'^api/v1/authuser/pics/(?P<pic_id>\d{1,11}).json$',
        dtrprofile.views_profile.profile_pics_item),
    url(r'^api/v1/authuser/pics.json$',
        dtrprofile.views_profile.profile_pics_list),
    url(r'^api/v1/authuser.json$',
        dtrprofile.views_profile.profile_api_view, kwargs={'use': 'authuser', 'q': None}),
    url(r'^api/v1/profile/(?P<q>[a-zA-Z0-9_-]{3,30}).json$',
        dtrprofile.views_profile.profile_api_view, kwargs={'use': 'username'}),
    url(r'^api/v1/user/(?P<q>\d{1,11}).json$',
        dtrprofile.views_profile.profile_api_view, kwargs={'use': 'user_id'}),

    # Search

    url(r'^api/v1/search.json$',
        dtrprofile.views_search.SearchAPIView.as_view(), name='search_api'),

    # Inbox/Messages

    url(r'^api/v1/inbox/(?P<t>recv|sent|unread|allread).json$',
        dtrprofile.views_inbox.InboxList.as_view(), name='inbox-list'),
    url(r'^api/v1/inbox/msg/(?P<pk>\d+).json$',
        dtrprofile.views_inbox.InboxItem.as_view(), name='inbox-item'),
    url(r'^api/v1/msgs/(?P<username>[a-zA-Z0-9_-]{3,30}).json$',
        dtrprofile.views_usermsg.UserMsgList.as_view(), name='usermsgs-list'),

    # Country/City

    url(r'^api/v1/all-countries.json$',
        city_views.all_countries, name='all_countries'),
    url(r'^api/v1/autocomplete-crc.json$',
        city_views.city_autocomplete_crc, name='city_autocomplete_crc'),
    url(r'^api/v1/cities-in-country.json$',
        city_views.cities_in_country, name='cities_in_country'),
    url(r'^api/v1/city-by-latlng.json$',
        city_views.city_by_latlng, name='city_by_latlng'),

    # SEO

    url(r'^browse\.php$',
        seo_views.users_alphabetically, name='dtrseo_users_alphabetically'),
    url(r'^mujeres-buscando-hombres\.php$',
        seo_views.users_f_m, name='dtrseo_users_f_m'),
    url(r'^hombres-buscando-mujeres\.php$',
        seo_views.users_m_f, name='dtrseo_users_m_f'),
    url(r'^fotos-mujeres\.php$',
        seo_views.users_f_pics, name='dtrseo_users_f_pics'),
    url(r'^fotos-hombres\.php$',
        seo_views.users_m_pics, name='dtrseo_users_m_pics'),
    url(r'^citymx(?P<city_short>[a-z]{3})/(?P<city_name>[a-zA-Z0-9_-]+)\.html$',
        seo_views.citymx, name='dtrseo_citymx'),
    url(r'^gente-por-pais\.php$',
        seo_views.country_list, name='dtrseo_country_list'),
    url(r'^paises/(?P<country>[a-z\-]{4,60})/$',
        seo_views.users_by_country, name='dtrseo_users_by_country'),
    url(r'^paises/(?P<country>[a-z\-]{4,60})/(?P<region>[0-9a-z\-]{2,60})/$',
        seo_views.users_by_country_region,
        name='dtrseo_users_by_country_region'),
    url(r'^paises/(?P<crc_url>[a-z-]{2,60}/[0-9a-z-]{2,80}/[0-9a-z-]{2,80})/$',
        seo_views.users_by_altname_url, name='dtrseo_users_by_altname_url'),
    # url(r'^thread/[a-zA-Z0-9-]+-(?P<threadid>\d+)-\d+\.html$',
    #    seo_views.redir_old_forum_threads,
    #    name='dtrseo_redir_old_forum_threads'),
    # url(r'^forum-archive\.php$',
    #    seo_views.forum_archive, name='dtrseo_forum_archive'),
    # Previous user profiles, do not implement!
    # url(r'^user/(?P<username>[a-zA-Z0-9-_]+)/?$',
    #    seo_views.redir_old_user_pages, name='dtrseo_redir_old_user_pages'),
    # url(r'^user/(?P<username>[a-zA-Z0-9-_]+)/fotos/\d{1,10}$',
    #    seo_views.redir_old_user_pages),
    # url(r'^user/(?P<username>[a-zA-Z0-9-_]+)/forum\d{1,3}\.html$',
    #    seo_views.redir_old_user_pages),
    # url(r'^user/(?P<username>[a-zA-Z0-9-_]+)/liguelog/.+$',
    #    seo_views.redir_old_user_pages),
]

# Django RESTframework automatic API URLs not used.
# rest_urlpatterns = format_suffix_patterns(rest_urlpatterns)

if not settings.PRODUCTION:
    app_path = os.path.join(settings.BASE_DIR, '..', 'dtr4-ui')

    # noinspection PyUnusedLocal
    def app_base_view(request):
        f = os.path.join(app_path, 'dist', request.path.lstrip('/'))
        mime = 'text/html'

        if os.path.isfile(f):
            print('FILE EXISTS: {}'.format(f))
            if f.endswith('.js'):
                mime = 'application/javascript'
            elif f.endswith('.css'):
                mime = 'text/css'
            elif f.endswith('.woff'):
                mime = 'application/font-woff'
            elif f.endswith('.ttf'):
                mime = 'application/font-sfnt'
        else:
            print('FILE NOT FOUND: {}'.format(f))
            f = os.path.join(app_path, 'dist', 'app', 'index.html')

        with open(f, 'rb') as fh:
            return HttpResponse(fh.read(), content_type=mime)

    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^app/', app_base_view)]
