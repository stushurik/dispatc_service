from django.db import models

# Create your models here.


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars')