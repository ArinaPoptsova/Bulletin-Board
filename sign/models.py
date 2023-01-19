from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    code = models.PositiveIntegerField(null=True, blank=True)
