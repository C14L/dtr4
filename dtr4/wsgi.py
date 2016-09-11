import os
from django.core.wsgi import get_wsgi_application

# TODO: this should not be needed.
# sys.path.append('/opt/elligue/dtr4')
# sys.path.append('/opt/elligue/dtr4/dtr4')

# Tell Django where to find the settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtr4.settings")
application = get_wsgi_application()
