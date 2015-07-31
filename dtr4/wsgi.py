# -*- coding: utf-8 -*-

"""
WSGI config for dtr4 project.
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the app's directory to the PYTHONPATH
sys.path.append('/opt/elligue/dtr4')
sys.path.append('/opt/elligue/dtr4/dtr4')
# Tell Django where to find the settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtr4.settings")
application = get_wsgi_application()
