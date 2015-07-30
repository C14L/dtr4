import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import user_signed_up, user_logged_in

from dtrflag.models import Flag, flag_changed, flag_pre_change
from dtrprofile.models import UserStatus, UserProfile, UserPic

@receiver(user_signed_up)
def user_signed_up_callback(sender, **kwargs):
    """
    Receiver for a signal from "allauth" module. Add an initial status message 
    about the signup to the Talk stream.

    Not used yet.
    """
    user = kwargs['user']
    msg = _("#Welcome @{username} from #{city} #{country}. "
            "Use hashtag #Intro to indroduce yourself!".format(
            {'username':'', 'city':'', 'country':''}))
    # >> TODO: UserStatus.autopost(user, msg, hidden=False)

@receiver(user_logged_in)
def user_logged_in_callback(sender, **kwargs):
    """
    Receiver for a signal from "allauth" module.

    Not used yet.
    """
    user = kwargs['user']
