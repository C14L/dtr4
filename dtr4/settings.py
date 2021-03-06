import os
import re
import pymysql
from dtr4 import settings_private

pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.path.exists('/islocal.txt')
PRODUCTION = not DEBUG

ENABLE_PROFILER = False
ENABLE_DEBUG_TOOLBAR = False

SECRET_KEY = settings_private.SECRET_KEY
ADMINS = settings_private.ADMINS
MANAGERS = settings_private.MANAGERS
DATABASES = settings_private.DATABASES
if not PRODUCTION:
    DATABASES['default']['USER'] = 'root'
    DATABASES['default']['PASSWORD'] = 'pla'

SITE_ID = 1
CSRF_COOKIE_NAME = 'csrftoken'  # default
CSRF_COOKIE_HTTPONLY = False  # needs access from Angular
CSRF_COOKIE_SECURE = True  # set True for HTTPS
if not PRODUCTION:
    CSRF_COOKIE_SECURE = False  # not on localhost

X_FRAME_OPTIONS = 'DENY'  # never serve any part in a frame; default: SAMEORIGIN
ROOT_URLCONF = 'dtr4.urls'
WSGI_APPLICATION = 'dtr4.wsgi.application'
SIMULATE_NETWORK_DELAY = False  # my own Middleware for API delay.
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'es'
LANGUAGE = LANGUAGE_CODE[:2]  # I added this. Remove?
LANGUAGE_COOKIE_NAME = 'lg'  # language cookie, default: "django_language"
# LANGUAGE_SESSION_KEY = None
# Suggested in: https://docs.djangoproject.com/en/1.7/topics/i18n/translation/
# Do not change! E.g. used to import geonames, all languages a user can select.
LANGUAGES = [
    ('en', 'English'), ('es', 'Español'),
]

# Paths to translations files.
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'dtr4/locale'),
    os.path.join(BASE_DIR, 'dtrseo/locale'),
]

ALLOWED_HOSTS = ['www.elligue.com', 'localhost']

# Block bad User-Agents, list of regexps. default: ()
# Do this in Apache2 .htaccess file, these should not even make it here.
DISALLOWED_USER_AGENTS = [
    re.compile('slurp', re.I),
    re.compile('baidu', re.I),
    re.compile('yandex', re.I),
    re.compile('curl', re.I),
    re.compile('wget', re.I),
]

# Don't email 404 error reports to ADMINS/MANAGERS for URLs that match these.
# See https://docs.djangoproject.com/en/1.8/howto/error-reporting/ and
# below the Middleware "django.middleware.common.BrokenLinkEmailsMiddleware".
IGNORABLE_404_URLS = (re.compile(r'\.(php|cgi)$'), re.compile(r'/wp-admin/'),
                      re.compile(r'/phpmyadmin/'),
                      re.compile(r'^/apple-touch-icon.*\.png$'), )
PREPEND_WWW = False  # done by Apache2 in production, unused on dev.
APPEND_SLASH = True
if PRODUCTION:
    SECURE_BROWSER_XSS_FILTER = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required for allauth.
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'channels',
    'dtrcity',
    'dtrprofile',
    'dtrseo',
]

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # My own: check if authuser was deleted and remove their session.
    'dtrprofile.middleware.CheckAuthUserAccountIsActive',
    # My own: update UserProfile.last_active for authuser.
    'dtrprofile.middleware.UserProfileLastActiveMiddleware',
    # My own: try to intercept spam bots.
    'dtrprofile.middleware.SimpleSpamBotTrapMiddleware',
    # My own: during development, simulate some network delay if
    # setting "SIMULATE_NETWORK_DELAY" is True.
    'dtrprofile.middleware.SimulateNetworkDelayMiddleware',
]

if ENABLE_PROFILER:
    MIDDLEWARE_CLASSES.insert(0, 'dtrprofile.middleware.ProfilerMiddleware')

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of allauth
    "django.contrib.auth.backends.ModelBackend",
    # allauth specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
                # allauth specific context processors
                # 'sites.allauth.account.context_processors.account',
                # 'sites.allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "dtr4.routing.channel_routing",
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

if not PRODUCTION:
    pass
    # The Angular app is here. On the live system, the app is served by
    # nginx directly, same as the other static files.
    # STATICFILES_DIRS = (
    #     # os.path.join(BASE_DIR, '../dtr4-ui'),
    #     # os.path.join(BASE_DIR, '../www'),
    # )

# Email config
EMAIL_SUBJECT_PREFIX = 'El Ligue: '  # For system emails to ADMINS+MANAGERS.
SERVER_EMAIL = settings_private.SERVER_EMAIL
DEFAULT_FROM_EMAIL = SERVER_EMAIL  # For emails to users.

EMAIL_HOST = settings_private.EMAIL_HOST
EMAIL_HOST_USER = settings_private.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings_private.EMAIL_HOST_PASSWORD

EMAIL_PORT = 25  # 587
EMAIL_USE_TLS = True
# EMAIL_USE_TLS = None
# EMAIL_USE_SSL = None
# EMAIL_SSL_KEYFILE
# EMAIL_SSL_CERTFILE

if PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # default
else:
    # Log to console on dev
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
   'default': {
       'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
       'LOCATION': '127.0.0.1:11211',
   },
}

# Session config
SESSION_COOKIE_DOMAIN = 'elligue.com'
SESSION_COOKIE_AGE = 60*60*24*30*12  # 1y
# SESSION_COOKIE_NAME = 'sessionid'
# SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = True  # Set to True when using HTTPS
if not PRODUCTION:
    SESSION_COOKIE_SECURE = False  # not on localhost
    SESSION_COOKIE_DOMAIN = None  # no restriction on dev
# For memcached use 'django.contrib.sessions.backends.cache'
# Django default: 'django.contrib.sessions.backends.db'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'

# AllAuth settings
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/app/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True  # allauth
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}
ACCOUNT_UNIQUE_EMAIL = False  # allow multiple accounts with same email.
ACCOUNT_AUTHENTICATION_METHOD = "username"  # login username only
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_SIGNUP_FORM_CLASS (=None) Ask the user for more info on signup
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 3
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'administrator', 'administrador',
                              'moderator', 'moderador', 'mod', ]
# My own account adapter to limit usernames to [a-zA-Z0-9_] only.
ACCOUNT_ADAPTER = 'dtrprofile.account_adapter.MyAccountAdapter'

# dtrprofile
# Show user as "online" if they were active within this time
ONLINE_SECONDS_SINCE_LAST_ACTIVE = 60 * 3
# Show user as "idle" if they were active within this time
IDLE_SECONDS_SINCE_LAST_ACTIVE = 60 * 10
# default page size for Talk lists.
DTR_TALK_PAGE_SIZE = 10

# User uploaded picture files
if PRODUCTION:
    MEDIA_ROOT = '/var/www/www.elligue.com/userpics'
    MEDIA_URL = '/pics/'
    # 'http://userpics.elligue.com/' # TODO: make it a subdomain!
else:
    MEDIA_ROOT = '/home/chris/dev-data/elligue/userpics'
    MEDIA_URL = '/pics/'
# TODO: This is probably not used currently. Implement watermarking and
# remove unused settings.
THUMBS_MINSIZE = (350, 350)  # ????                     # Orig uploaded files
THUMBS_ORIGINAL_DIR = os.path.join(MEDIA_ROOT, 'orig')  # <-- before resizing.
THUMBS_WATERMARK_IMAGES = {
    '350x350': os.path.join(BASE_DIR, 'misc/watermark_elligue1.png')
}
# The maximum size, in Bytes, for files that will be uploaded into memory. Files
# larger than FILE_UPLOAD_MAX_MEMORY_SIZE will be streamed to disk.
# Default: 2621440 Bytes (2.5 MiB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10000000  # 10 MB
# The directory where uploaded files larger than FILE_UPLOAD_MAX_MEMORY_SIZE
# will be stored. Django default: /tmp
# FILE_UPLOAD_TEMP_DIR = ''
# The numeric mode (i.e. 0644) to set newly uploaded files to. For more info
# about what these modes mean, see the documentation for os.chmod(). If this
# isn’t given or is None, you’ll get operating-system dependent behavior. On
# most platforms, temporary files will have a mode of 0600, and files saved
# from memory will be saved using the system’s standard umask.
# FILE_UPLOAD_PERMISSIONS = 0644

# REST framework settings
# See http://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
}
