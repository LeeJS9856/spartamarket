from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=100, null=True, blank=False)
