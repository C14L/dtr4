from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import enforce_ordering


def get_group_name_for_user(user):
    """Returns a unique deterministic group name for every user."""
    return 'user-{}'.format(user.username)


def get_common_group_name():
    """Return the name of the common group all connected users belong to."""
    return 'talk_channel'


@enforce_ordering(slight=True)
@channel_session_user_from_http
def ws_connect(message):
    user_devices = get_group_name_for_user(message.user)
    Group(user_devices).add(message.reply_channel)
    Group(get_common_group_name()).add(message.reply_channel)


@enforce_ordering(slight=True)
@channel_session_user
def ws_message(message):
    user_devices = get_group_name_for_user(message.user)
    Group(user_devices).send({"text": message['text']})


@enforce_ordering(slight=True)
@channel_session_user
def ws_disconnect(message):
    user_devices = get_group_name_for_user(message.user)
    Group(user_devices).discard(message.reply_channel)
    Group('talk_channel').add(message.reply_channel)


"""

For now, use the current funcitons in views.py to receive Talk and Inbox
messages via HTTP and then sent them to the appropriate channel, either the
individual user's channel, or the common `talk_channel`.

Once that works, a second step would be to use WS also for sending, and to
implement the entire send/receive logic here. More on that tomorrow...

"""
