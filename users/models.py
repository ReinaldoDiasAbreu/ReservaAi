from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cargo = models.TextField(max_length=20, blank=False)
