import json
from datetime import datetime

import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponseBadRequest, HttpResponseForbidden, \
    HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import utc
from django.views.decorators.http import require_http_methods

from dtrprofile.models_flag import UserFlag
from dtrprofile.models_talk import Talk, TalkHashtag, TalkUsername


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
