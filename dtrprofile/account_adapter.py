import re
from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import get_user_model
from django import forms
from django.utils.translation import ugettext_lazy as _

# USERNAME_REGEX = re.compile(r'^[\w.@+-]+$', re.UNICODE)
# The new regexp, sans the special chars.
USERNAME_REGEX = re.compile('^[a-zA-Z0-9_]+$', re.UNICODE)


class MyAccountAdapter(DefaultAccountAdapter):
    """
    This overrides the default account adapter class for the AllAuth app found
    at allauth.account.adapter.DefaultAccountAdapter and changes the valid
    characters for usernames. Usernames may only contain [A-Za-z0-9_]
    """

    def __init__(self, *args, **kwargs):
        super(MyAccountAdapter, self).__init__(*args, **kwargs)

    def clean_username(self, username, shallow=False):
        if not USERNAME_REGEX.match(username):
            ret = _("Usernames can only contain letters, digits and @/./+/-/_.")
            ret = ret.replace("@/./+/-/", "")  # Remove the special chars from
            raise forms.ValidationError(ret)   # the translation we got here.

        # Below is copy-paste from the original method. See source at
        # https://github.com/pennersr/django-allauth/blob/master/allauth/account/adapter.py#L207

        username_blacklist_lower = [ub.lower() for ub in getattr(
            app_settings, 'USERNAME_BLACKLIST', [])]

        if username.lower() in username_blacklist_lower:
            raise forms.ValidationError(_("Username can not be used. "
                                          "Please use other username."))

        username_field = getattr(app_settings, 'USER_MODEL_USERNAME_FIELD',
                                 'username')
        assert username_field
        user_model = get_user_model()

        try:
            query = {username_field + '__iexact': username}
            user_model.objects.get(**query)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError(_("This username is already taken. Please "
                                      "choose another."))
