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


def usermsg_init():
    pass
    # TODO: Return an initial list of past messages between the users.
    #       Currently still done via HTTP.


def usermsg_receive():
    pass
    # sender_group = get_group_name_for_user(request.user)
    # receiver_group = get_group_name_for_user(user)
    # resp = {'action': 'usermsg.receive', 'msg_list': [serializer.data]}
    # ChannelsGroup(sender_group).send({'text': json.dumps(resp)})
    # ChannelsGroup(receiver_group).send({'text': json.dumps(resp)})
