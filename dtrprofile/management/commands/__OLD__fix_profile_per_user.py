# -*- encoding: utf-8 -*-

""" 
Make sure that every User has a UserProfile. Create it if necessary.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from dtrprofile.models_profile import UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):

        for user in User.objects.all():

            p, created = UserProfile.objects.get_or_create(user=user)
            if created:
                print '\rUserProfile for "{}" ({}) created.    '.format(user.username, user.id)
            else:
                print '\r{}                                    '.format(user.username),

