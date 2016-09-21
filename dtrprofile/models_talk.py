from django.contrib.auth.models import User
from django.db import models


class Talk(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             db_index=True, related_name='talks')
    created = models.DateTimeField()
    created_ip = models.CharField(default='', max_length=15)
    parent = models.ForeignKey('self', db_index=True, null=True,
                               default=None, related_name='children')
    child_counter = models.SmallIntegerField(default=0)
    views_counter = models.SmallIntegerField(default=0)
    hashtag_counter = models.SmallIntegerField(default=0)
    username_counter = models.SmallIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    text = models.TextField()

    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super(Talk, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.text


class TalkHashtag(models.Model):
    # the hashtag withOUT the "#" hash.
    tag = models.CharField(max_length=50, db_index=True)
    # ref to talk post id
    talk = models.ForeignKey(Talk, db_index=True, related_name="hashtag")


class TalkUsername(models.Model):
    user = models.ForeignKey(User, db_index=True, related_name="mentioned_in")
    talk = models.ForeignKey(Talk, db_index=True, related_name="mentions")