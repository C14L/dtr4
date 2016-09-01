from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


# noinspection PyUnusedLocal
@receiver(user_signed_up)
def user_signed_up_callback(sender, **kwargs):
    """
    Receiver for a signal from "allauth" module. Add an initial status message 
    about the signup to the Talk stream.

    Not used yet.
    """
    user = kwargs['user']
    msg = _("#Welcome @{username} from #{city} #{country}. "
            "Use hashtag #Intro to indroduce yourself!"
            "".format({'username': '', 'city': '', 'country': ''}))
    # >> TODO: UserStatus.autopost(user, msg, hidden=False)


# noinspection PyUnusedLocal
@receiver(user_logged_in)
def user_logged_in_callback(sender, **kwargs):
    """
    Receiver for a signal from "allauth" module.

    Not used yet.
    """
    user = kwargs['user']
