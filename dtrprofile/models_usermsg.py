from django.contrib.auth.models import User
from django.db import models

from dtrprofile.utils import nowtime


class UserMsg(models.Model):
    """Store private messages between users."""

    from_user = models.ForeignKey(User, related_name='msg_sent',
                                  null=True, on_delete=models.SET_NULL)
    to_user = models.ForeignKey(User, related_name='msg_received',
                                null=True, on_delete=models.SET_NULL)
    # Set True when user opens profile page and messages are displayed.
    is_read = models.BooleanField(default=False)
    # Set True if user replies or manually sets it to "done".
    is_replied = models.BooleanField(default=False)
    # Set True if the sending user was blocked by receiver.
    # TODO: remove and handle in UserFlag only!
    is_blocked = models.BooleanField(default=False)
    # Time and IP the message was sent.
    created = models.DateTimeField()
    created_ip = models.CharField(default='', max_length=15, blank=True)
    # The actual text of the message.
    text = models.TextField()

    class Meta:
        index_together = [['from_user', 'to_user'], ['to_user', 'from_user']]

    def __str__(self):
        s = 'Message [{}] from "{}" ({}) to "{}" ({}) on "{}".'
        return s.format(self.id, self.from_user.username, self.from_user.id,
                        self.to_user.username, self.to_user.id, self.created)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = nowtime()
        super(UserMsg, self).save(*args, **kwargs)

    @classmethod
    def set_is_read_all(cls, to_user):
        """Set all messages received by 'to_user' to is_read=True."""
        for row in UserMsg.objects.filter(to_user=to_user, is_read=False):
            # TODO: there's a more efficient way to do this!
            # "bulk update" something.
            row.is_read = True
            row.save()

    @classmethod
    def set_is_read(cls, from_user, to_user):
        """Set all msgs by 'from_user' to 'to_user' to is_read=True."""
        for row in UserMsg.objects.filter(from_user=from_user, to_user=to_user):
            # TODO: there's a more efficient way to do this!
            # "bulk update" something.
            row.is_read = True
            row.save()

    @classmethod
    def unset_is_read(cls, from_user, to_user):
        """Sets *last* msg by from_user to to_user to is_read=False."""
        msg = UserMsg.objects.filter(from_user=from_user, to_user=to_user)\
                             .order_by('-created').first()
        if msg is not None:
            msg.is_read = False
            msg.save()


