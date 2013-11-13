from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField, ForeignKey, TextField

from core.models import MinMaxFloat


class Event(models.Model):

    class Meta:
        permissions = (
            ("view_events", "Can see available events"),
        )

    created = DateTimeField(auto_now_add=True)
    author = ForeignKey(User, null=False, related_name='authors_set')
    executor = ForeignKey(User, null=False, related_name='executors_set')
    priority = MinMaxFloat(min_value=0.0, max_value=100.0, default=50.0)

    #decision = OneToOneField(Decision, null=True)
    description = TextField(null=False, blank=True)

    def __unicode__(self):
        return "Event #%s - p%s - date:%s - author:%s" % \
               (self.id, self.priority, self.created, self.author)
