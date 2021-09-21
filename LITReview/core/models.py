from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


class CustomUser(AbstractUser):
    """

    """
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user_view', kwargs={'user_id': self.id})
