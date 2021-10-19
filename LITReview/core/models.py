from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


class CustomUser(AbstractUser):
    """
    Extends the Basic User class without adding anything to it
    in order to be able to override it easily in the future, if needed
    """
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user_view', kwargs={'user_id': self.id})
