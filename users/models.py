from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    tipo_usuario = models.TextField(max_length=20, blank=False)
    telefone = models.TextField(max_length=15, blank=True)
