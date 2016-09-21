import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect  # 301
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from dtrprofile.models_profile import UserPic


def homepage(request, template_name="dtrprofile/site_index.es.html"):
    """The homepage view at "/".

    If the user is logged in, simply redirect to the app's startpage.

    Otherwise, serve a HTML page with forms for login and signup, as
    well as some text content describing the purpose of the site, both
    for SEO and for the user.
    """
    # Authenticated user load app
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect(settings.LOGIN_REDIRECT_URL)
    # Anon users get a nice home page.
    return render(request, template_name)


@login_required
@require_http_methods(['GET'])
def pictures_list(request):
    """
    Return a list of most recent user uploaded pictures items. Each item is a
    dict with the fields: id, username, created

    Optionally params: count - number of items to return, between 1 and 500.
                       below_id - only return pics with IDs smaller than this.
    """
    data = []
    count = int(request.GET.get('count', 50))
    below_id = int(request.GET.get('below_id', 0))
    if not count or count < 1 or count > 500:
        count = 50
    pics = UserPic.objects.all().order_by('-created').select_related('user')
    if below_id:
        pics = pics.filter(id__lt=below_id)
    for pic in pics[:count]:
        data.append({'id': pic.id,
                     'username': pic.user.username,
                     'created': pic.created.isoformat()})
    return HttpResponse(json.dumps(data), {'content_type': 'application/json'})
