# -*- coding: utf-8 -*-

"""
WSGI config for dtr4 project.
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Fallback to print some error message
some_error = 'ALL OKAY!'
def errapp(env, start_response):
    from datetime import datetime
    from django import get_version as django_version
    global some_error
    data = "<ul><li>{2}<li>Python: '{0}'<li>Django: '{3}'<li>some error happened: '{1}'</ul>".format(
        sys.version, some_error, datetime.now(), django_version())
    start_response("200 OK", [("Content-Type", "text/html")])
    return [data]

# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/opt/elligue/venv/dtr4/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/opt/elligue/dtr4')
sys.path.append('/opt/elligue/dtr4/dtr4')

# Tell Django where to find the settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtr4.settings")

# Activate your virtual environment
#activate_env = "/opt/elligue/venv/dtr4/bin/activate_this.py"
#execfile(activate_env, dict(__file__=activate_env))

try:
    application = get_wsgi_application()
except Exception as e:
    some_error = e
    application = errapp
