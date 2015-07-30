"""
WSGI config for dtr4 project.
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtr4.settings")
application = get_wsgi_application()

#def application(env, start_response):
#    start_response('200 OK', [('Content-Type','text/html')])
#    return ["Hello World"]

