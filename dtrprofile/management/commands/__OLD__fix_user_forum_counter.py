# -*- encoding: utf-8 -*-

""" 

For each user profile, count all sorts of things in the forums:

- forum_boards_admin_counter      Forum boards owned by user.
- forum_boards_moderator_counter  Forum boards moderated by user.
- forum_boards_member_counter     Forum boards user is a member of.
- forum_boards_banned_counter     Forum boards that banned user.

- forum_threads_counter           Forum thread posts by user.
- forum_replies_counter           Forum reply posts by user.
- forum_posts_moderated_counter   Forum posts by user deleted by moderators.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from dtrprofile.models_profile import UserProfile
from dtrforum.models import Board, Post, BoardMember
from dtrglue import utils

class Command(BaseCommand):

    def handle(self, *args, **options):

        for userprofile in UserProfile.objects.all().prefetch_related('user'):

            # Forum boards owned by user.
            for boardmember in BoardMember.objects.filter(user=userprofile.user):
                if boardmember.is_admin(): 
                    userprofile.forum_boards_admin_counter += 1
                if boardmember.is_moderator(): 
                    userprofile.forum_boards_moderator_counter += 1
                if boardmember.is_banned(): 
                    userprofile.forum_boards_banned_counter += 1
                else:
                    userprofile.forum_boards_member_counter += 1

            # Thread starter and reply posts, and posts deleted by moderators.
            for post in Post.objects.filter(user=userprofile.user):
                if post.has_status('DELETED'): # Count posts deleted by ...
                    if post.has_status('MODERATED'): # ... moderators only.
                        userprofile.forum_posts_moderated_counter += 1
                else: # Not deleted, only count life posts.
                    if post.thread is None: # Thread starters
                        userprofile.forum_threads_counter += 1
                    else: # Reply posts
                        userprofile.forum_replies_counter += 1

            userprofile.save()

            print 'User {} -- Board of {}, moderator in {}, and member in {} boards. Was banned from {} boards.'.format(
                userprofile.user.id,
                userprofile.forum_boards_admin_counter,
                userprofile.forum_boards_moderator_counter,
                userprofile.forum_boards_member_counter,
                userprofile.forum_boards_banned_counter )
            print '        -- Started {} threads and wrote {} replies to threads. Had {} posts deleted by moderators.'.format(
                userprofile.forum_threads_counter,
                userprofile.forum_replies_counter,
                userprofile.forum_posts_moderated_counter )
