from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField, TextField, ForeignKey


class Decision(models.Model):
    created = DateTimeField(auto_now_add=True)
    description = TextField(blank=False)
    author = ForeignKey(User, null=False)
