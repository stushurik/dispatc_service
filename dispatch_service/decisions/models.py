from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField, TextField, ForeignKey, OneToOneField
from events.models import Event


class Decision(models.Model):
    class Meta:
        permissions = (
            ("view_decisions", "Can see available decisions"),
        )

    created = DateTimeField(auto_now_add=True)
    description = TextField(blank=False)
    author = ForeignKey(User, null=False)
    deadline = DateTimeField(null=False)

    event = OneToOneField(Event)
