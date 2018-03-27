from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class User(models.Model):

    username = models.OneToOneField(User)

    role = models.TextField(
        max_length=50,
        verbose_name='Role',
        blank=True
    )

    def __str__(self):
        return self.first_name