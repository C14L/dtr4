from channels import Group
from channels.sessions import channel_session


def get_group_name_for_user(user):
    """Returns a unique deterministic group name for every user."""
    return 'user-{}'.format(user.username)


@channel_session
def ws_connect(message):
    user_devices = get_group_name_for_user(message.user)
    Group(user_devices).add(message.reply_channel)
    Group('talk_channel').add(message.reply_channel)


@channel_session
def ws_message(message):
    user_devices = get_group_name_for_user(message.user)
    Group(user_devices).send({"text": message['text']})


@channel_session
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
