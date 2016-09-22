from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.timezone import utc

from dtrprofile.models_usermsg import UserMsg
from dtrprofile.utils import nowtime

USERFLAG_IS_ONE_WAY = False
USERFLAG_IS_TWO_WAY = True
USERFLAG_TYPES = (
    # mutual, invite/confirm "friend" relationship
    (1, 'friend',   USERFLAG_IS_TWO_WAY),
    # mutual, like and like back to get a romantic "match".
    (2, 'like',     USERFLAG_IS_TWO_WAY),
    # block another user so they can't see my profile or send messages anymore.
    (3, 'block',    USERFLAG_IS_ONE_WAY),
    # you can only have 5 favorites at a time!
    (4, 'favorite', USERFLAG_IS_ONE_WAY),
    # last time sender viewed the profile of receiver.
    (5, 'viewed',   USERFLAG_IS_ONE_WAY),
)
USERFLAG_TYPES_CHOICES = [(x[0], x[1]) for x in USERFLAG_TYPES]


class UserFlag(models.Model):
    """Set flags between user profiles: fav, like/match, block."""

    sender = models.ForeignKey(
        User, db_index=True, related_name='has_flagged')
    receiver = models.ForeignKey(
        User, db_index=True, related_name='was_flagged')
    flag_type = models.PositiveIntegerField(choices=USERFLAG_TYPES_CHOICES)
    # Time the flag was set.
    created = models.DateTimeField(default=nowtime())
    # Time mutual flag was set for reciprocal relations.
    confirmed = models.DateTimeField(default=None, null=True)

    class Meta:
        index_together = [
            ['sender', 'receiver'],
            ['receiver', 'sender'],
            ['flag_type', 'receiver', 'sender'],
            ['flag_type', 'sender', 'receiver'],
        ]
        unique_together = ['sender', 'receiver', 'flag_type']

    def __init__(self, *args, **kwargs):
        super(UserFlag, self).__init__(*args, **kwargs)

    def __str__(self):
        s = 'Flag {0}: by {1} to {2} type "{3}".'
        return s.format(self.pk, self.sender.username,
                        self.receiver.username, self.flag_type)

    @classmethod  # TODO: DELETE THIS??
    def get_flags(cls, user1, user2):
        return UserFlag.objects.filter(sender=user1, receiver=user2)

    @classmethod
    def last_viewed(cls, user1, user2):
        """Return date of the last "viewed" flag, or None if never."""
        f = UserFlag.objects.filter(sender=user1, receiver=user2, flag_type=5)
        if f:
            return f[0].created
        else:
            return None

    @classmethod
    def all_between_users(cls, user1, user2):
        """Return all flags between two users."""
        return UserFlag.objects.filter(Q(sender=user1, receiver=user2) |
                                       Q(sender=user2, receiver=user1))

    @classmethod
    def get_one_way_flags(cls, user1, user2):
        """Return all one-way flags between two users."""
        one_way_choices = [y[0] for y in USERFLAG_TYPES if not y[2]]
        return UserFlag.all_between_users(user1, user2)\
                       .filter(flag_type__in=one_way_choices)

    @classmethod
    def get_two_way_flags(cls, user1, user2):
        """Return all two-way flags between two users."""
        two_way_choices = [y[0] for y in USERFLAG_TYPES if y[2]]
        return UserFlag.all_between_users(user1, user2)\
                       .filter(flag_type__in=two_way_choices)

    @classmethod
    def get_flag(cls, flag_name, user1, user2):
        """Return a specific flag between two users.

        flag_name: one of the defined flag names, e.g. "like", "block".
        user1, user2: django.auth.models.User objects.

        Raise DoesNotExist exception if the flag doesn't exist.
        """
        try:
            # Find the flag name in the USERFLAG_TYPES list.
            flag_type, two_way_flag = [(y[0], y[2]) for y in
                                       USERFLAG_TYPES if y[1] == flag_name][0]
        except IndexError:
            raise AttributeError('No flag by this name.')
        # Fetch exactly one object, anything else would be an exception.
        return UserFlag.objects.get(Q(sender=user1, receiver=user2) |
                                    Q(sender=user2, receiver=user1),
                                    flag_type=flag_type)

    @classmethod
    def get_flag_type(cls, flag_name):
        """Return [flag_type, flag_name, two_way_flag] by flag name."""
        return [x for x in USERFLAG_TYPES if x[1] == flag_name][0]

    @classmethod
    def set_flag(cls, flag_name, sender, receiver):

        flag_type, flag_name, two_way_flag = cls.get_flag_type(flag_name)

        # Check if flag or confirm already exists.
        flag = None
        try:
            flag = UserFlag.objects.get(flag_type=flag_type,
                                        sender=sender, receiver=receiver)
        except UserFlag.DoesNotExist:
            pass

        # If not and this is two-way, check if authuser confirmed a flag
        if flag is None and two_way_flag:
            try:
                flag = UserFlag.objects.get(flag_type=flag_type,
                                            sender=receiver, receiver=sender)
            except UserFlag.DoesNotExist:
                pass

        # If no flag exists yet, add a new flag
        if flag is None:
            flag = UserFlag()
            flag.flag_type = flag_type
            flag.sender = sender
            flag.receiver = receiver
            flag.created = datetime.utcnow().replace(tzinfo=utc)
            flag.save()

        # or for two-way, if there was an unconfirmed flag, confirm it
        elif flag is not None and flag.sender == receiver \
                and not flag.confirmed:
            flag.confirmed = datetime.utcnow().replace(tzinfo=utc)
            flag.save()

        if flag_name == 'block':
            # EVIL SHORTCUT!!! if "block" flag is set, set "UserMsg.is_blocked"
            # on all msgs that have authuser as "to_user", user as "from_user".
            # TODO: Remove this and lookup the "blocked" status between users
            # each time messages are loaded.
            UserMsg.objects.filter(to_user=sender,
                                   from_user=receiver).update(is_blocked=True)

    @classmethod
    def remove_flag(cls, flag_name, sender, receiver):

        flag_type, flag_name, two_way = UserFlag.get_flag_type(flag_name)

        flag = UserFlag.get_flag(flag_name, sender, receiver)

        if two_way:
            if flag.receiver == sender and flag.confirmed:
                flag.confirmed = None
                flag.save()

            elif flag.sender == sender:
                old_confirmed = flag.confirmed
                flag.delete()

                if flag.confirmed:
                    # if was confirmed, so we need to remove this flag, and set
                    # a new flag with the previous receiver as sender.
                    UserFlag.objects.create(
                        sender=receiver, receiver=sender,
                        flag_type=flag_type, created=old_confirmed)
        else:
            # for a one-way, just delete it.
            flag.delete()

        if flag_name == 'block':
            # EVIL SHORTCUT --> if "block" flag is removed, also remove all
            # "UserMsg.is_blocked" on msgs that have authuser as "to_user" and
            # user as "from_user".
            UserMsg.objects.filter(to_user=sender,
                                   from_user=receiver).update(is_blocked=False)
