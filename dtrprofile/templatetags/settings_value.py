
#
# Make all settings values accessible from any template.
#
# Example:
# {% settings_value "LANGUAGE_CODE" %}
#
# Adapted from 
# http://stackoverflow.com/questions/433162/can-i-access-constants-in-settings-py-from-templates-in-django
#

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
