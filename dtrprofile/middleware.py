import cProfile
import sys
from datetime import datetime
from time import sleep
from time import time

import os
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.timezone import utc
from random import random

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from django.conf import settings


class SimulateNetworkDelayMiddleware(object):
    """During development, simulate some network lag."""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, request):
        if settings.SIMULATE_NETWORK_DELAY and settings.DEBUG:
            max_secs = 3
            rand_secs = int(random() * max_secs) + 1
            print('SimulateNetworkDelayMiddleware: waiting for {} seconds...'
                  ''.format(rand_secs))
            sleep(rand_secs)
        return None


class UserProfileLastActiveMiddleware(object):
    """Updates the "last_active" field of the UserProfile model."""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, request):
        if request.user.is_authenticated():
            nowdt = datetime.utcnow().replace(tzinfo=utc)
            request.user.profile.last_active = nowdt
            request.user.profile.active_counter += 1  # F('active_counter') + 1
            request.user.profile.save(
                update_fields=['last_active', 'active_counter'])
        return None


class CheckAuthUserAccountIsActive(object):
    """When a user account gets deleted by a moderator, and the user is still
    authenticated, the session is not affected. This will stop a deleted user
    from continuously using a session."""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_active:
            return HttpResponseBadRequest('Your account was deleted.')
        return None


class SiteTemporarilyOffline(object):
    """Checks for the settings.SITE_OFFLINE_ENV_VARIABLE environment variable
    and if it holds a True value, then return a Http Temporarily Unavalable
    reply."""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, request):
        e = int(os.getenv(settings.SITE_OFFLINE_ENV_VARIABLE, 0))
        if e:
            return HttpResponse('We are back in a few minutes.')
        return None


class SimpleSpamBotTrapMiddleware(object):
    """Does a couple of checks to recognize spam bots."""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyPep8Naming
    def process_request(self, request):
        """
        1. In POST requests, looks for field name defined in
        SPAMBOT_TRAP_FIELD_NAME setting. If the field is *not* empty, assume
        that a spam bot filled in the field, because the field is hidden to
        normal users.
        """
        SPAMBOT_TRAP_FIELD_NAME = getattr(
            settings, 'SPAMBOT_TRAP_FIELD_NAME', 'spambotmiddlewaretoken')

        if request.method == 'POST':
            v = request.POST.get(SPAMBOT_TRAP_FIELD_NAME, False)
            if v:
                # SPAMBOT - bot trap form field not empty.
                return HttpResponseBadRequest('Please do not fill that field!')

        """
        2. Check the global frequency a user is posting. It saves the post times
        for the last 60 seconds in the user's session variable (if on memcached,
        there is no time penalty) and then checks if they fit into the limits
        set by SPAMBOT_MAX_POSTS_PER_MINUTE, SPAMBOT_MIN_SECONDS_BETWEEN_POSTS
        settings values.
        """
        # Set defaults if not set in settings.
        SPAMBOT_MAX_POSTS_PER_MINUTE = getattr(
            settings, 'SPAMBOT_MAX_POSTS_PER_MINUTE', 20)
        SPAMBOT_MIN_SECONDS_BETWEEN_POSTS = getattr(
            settings, 'SPAMBOT_MIN_SECONDS_BETWEEN_POSTS', 1)

        if request.method == 'POST':
            now = int(time())
            lim = now - 60  # one minute ago
            lp = request.session.get('spambot_last_posts', [])
            lp = [t for t in lp if t >= lim]  # remove all older than "lim"

            if len(lp) > SPAMBOT_MAX_POSTS_PER_MINUTE:
                # SPAMBOT - Too many posts per minute.
                return HttpResponseBadRequest(
                    'You posted too often in one minute. Please wait a little '
                    'and try again.')

            if len(lp) > 0:
                last = lp[-1]
                delta = now - last
                if delta < SPAMBOT_MIN_SECONDS_BETWEEN_POSTS:
                    # SPAMBOT - Time between posts too short.
                    return HttpResponseBadRequest(
                        'Not so fast. Please wait {0} seconds between posts.'
                        ''.format(SPAMBOT_MIN_SECONDS_BETWEEN_POSTS))
            else:
                pass

            # Add the time of this post request to the list of recent posts
            # and write the list back to the user's session.
            lp.append(now)
            request.session['spambot_last_posts'] = lp

        # If the request past all checks and filters, then return None to 
        # proceed.
        return None


class ProfilerMiddleware(object):
    profiler = None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.ENABLE_PROFILER and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.ENABLE_PROFILER and 'prof' in request.GET:
            self.profiler.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out
            self.profiler.print_stats(1)
            sys.stdout = old_stdout
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response
