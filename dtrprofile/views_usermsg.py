from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.utils.timezone import now as timezone_now
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dtrprofile.models_flag import UserFlag
from dtrprofile.models_usermsg import UserMsg
from dtrprofile.serializers import UserMsgSerializer


def can_send_msg(sender, receiver):
    """Returns True if sender has permission to message receiver.

    sender User object of message author, most likely request.user
    receiver User object of message receipient.
    """
    f_block = UserMsg.get_flag_type('block')
    return not UserFlag.objects.filter(
        # Careful: "receiver" of flag is "sender" of message.
        receiver=sender, sender=receiver, flag_type=f_block).exists()


def send_new_msg_email(request, user, msg):
    """Send a 'you have a new message' email.

    request The request context.
    user The receipient of the private message.
    msg The text string of the message.

    Verifies that the receipient has an email address in their
    account and that they have not received a "new message" email
    within a set amount of time.
    """
    # Default minimum time between two notification emails.
    gap_sec = 60 * getattr(settings, 'SEND_EMAIL_TIMEGAP_MINUTES', 60)
    gap_ok = ((not user.profile.last_email) or (timezone_now() -
              user.profile.last_email).total_seconds() > gap_sec)

    if user.email and gap_ok:
        from_user = request.user
        lg = get_language()[:2].lower()
        fn = 'dtrprofile/email_notify_new_private_message.{}'.format(lg)
        plaintext = get_template('{}.txt'.format(fn))
        # noinspection PyBroadException
        try:
            # optional html version
            htmltext = get_template('{}.html'.format(fn))
        except:
            htmltext = None

        d = Context({'user': user, 'from_user': from_user,
                     'msg': msg, 'site': get_current_site(request)})
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        subject, text_content = plaintext.render(d).split('\n\n', 1)
        html_content = None
        if htmltext:  # optional
            html_content = htmltext.render(d)
        email = EmailMultiAlternatives(subject, text_content,
                                       from_email, [to_email])
        if htmltext:  # optional
            email.attach_alternative(html_content, "text/html")
        email.send()

        # Remember the time when this email was sent.
        user.profile.last_email = timezone_now()
        user.profile.save()


def fetch_usermsgs(receiver, sender,
                   after=None, before=None, count=20):
    """Return a QuerySet of "count" messages between two users.

    If after or before is set, return only messages that were sent
    after/before that timestamp.

    The messages received by receiver are set to "is_read=True"
    automatically.
    """
    usermsgs = UserMsg.objects.filter(
        Q(from_user=receiver, to_user=sender) |
        Q(from_user=sender, to_user=receiver))
    if after:
        usermsgs = usermsgs.filter(created__gt=after)
    if before:
        usermsgs = usermsgs.filter(created__lt=before)
    # This will set all messages received by "to_user" and sent by
    # "from_user" to "is_read=True", because "to_user" as the
    # receipient has seen them now.
    UserMsg.set_is_read(from_user=sender, to_user=receiver)
    return usermsgs.order_by('-pk')[:count]


class UserMsgList(APIView):
    """
    Private messages between the authuser and one other user.

    To be displayed when the authuser views the other user's profile
    page.
    """

    @method_decorator(login_required)
    def get(self, request, username):
        usermsgs = fetch_usermsgs(
            request.user,
            get_object_or_404(User, username=username),
            request.GET.get('after', None),
            request.GET.get('before', None), 20)

        # TODO: Doesn't load older messages yet.

        serializer = UserMsgSerializer(usermsgs, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def post(self, request, username):
        """Send a private message from request.user to user."""

        after = request.POST.get('after', None)
        user = get_object_or_404(User, username=username)

        # Check if request.user has permission to message user.
        if not can_send_msg(request.user, user):
            return HttpResponseBadRequest('Can not send message.')

        # Expected values: text:<message text>
        data = request.data
        data['to_user'] = user.pk
        data['from_user'] = request.user.pk
        data['created'] = timezone_now()
        serializer = UserMsgSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            # Send notification email to receipient.
            send_new_msg_email(request, user, data['text'])

            # Return ALL posts since last check (after) NOT only this one.
            if after is None:
                # get the last ten or so to make sure we catch up.
                usermsgs = fetch_usermsgs(request.user, user, count=10)
            else:
                # return all messages after the last the user received.
                usermsgs = fetch_usermsgs(request.user, user, after)
            #
            # TODO: this should return all new messages since "after" but it
            #       doesn't for some reason. 2014-12-19
            #

            serializer = UserMsgSerializer(usermsgs, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Something went wrong in the serializer.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


