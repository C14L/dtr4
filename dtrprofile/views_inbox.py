import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dtrprofile.models_usermsg import UserMsg
from dtrprofile.serializers import InboxSerializer


class InboxList(APIView):
    """Return lists for unread, inbox, and sent messages.

    List all messages authuser has received (t=recv), has sent (t=sent)
    or all received messages not yet read (t=unread). GET[after] or
    GET[before] may have a timestamp to load only messages "created"
    before or after that time.
    """

    @method_decorator(login_required)
    def get(self, request, t=None):
        count = request.GET.get('count', 20)
        after = request.GET.get('after', None)
        before = request.GET.get('before', None)
        # Build the messages query
        usermsgs = UserMsg.objects.all().order_by('-created')
        # set what box to load
        if t == 'recv':
            usermsgs = usermsgs.filter(to_user=request.user, is_blocked=False)
        elif t == 'unread':
            usermsgs = usermsgs.filter(to_user=request.user,
                                       is_read=False, is_blocked=False)
        elif t == 'sent':
            usermsgs = usermsgs.filter(from_user=request.user)
        else:
            return Response([], status=status.HTTP_404_NOT_FOUND)
        # add time limits, if requested
        if before:
            usermsgs = usermsgs.filter(created__lt=before)
        elif after:
            usermsgs = usermsgs.filter(created__gt=after)
        # and finally serialize and return the list
        serializer = InboxSerializer(usermsgs[:count], many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def post(self, request, t=None):
        """Set all of authuser's received messages to "is_read"."""
        # TODO: use GET['read']==1 GET['replied']==1 here, to mirror the
        # setting for invididual messages below.
        if t == 'allread':
            UserMsg.set_is_read_all(request.user)
            return HttpResponse()
        else:
            return HttpResponseNotFound()


class InboxItem(APIView):
    """To set individual messages manually to is_read or is_replied."""

    @method_decorator(login_required)
    def post(self, request, pk):
        # decode json from body
        body = json.loads(request.body.decode("utf-8"))
        # either "1" or "0" to set or unset status.
        is_read = int(body.get('is_read', -1))
        is_replied = int(body.get('is_replied', -1))
        item = get_object_or_404(UserMsg, pk=pk, to_user=request.user)
        if is_read == 0:
            item.is_read = False
        if is_read == 1:
            item.is_read = True
        if is_replied == 0:
            item.is_replied = False
        if is_replied == 1:
            item.is_replied = True
        item.save()
        return HttpResponse()


