from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.forms import Form


class CustomUser(AbstractUser):
    """

    """
    def __str__(self):
        return self.username
