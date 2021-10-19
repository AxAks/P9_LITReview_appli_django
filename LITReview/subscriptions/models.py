from django.db import models

from LITReview import settings


# Create your models here.

class UserFollows(models.Model):
    """
    A Class handling the subscritpions between users:
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return f'{self.user} est abonné à {self.followed_user}'

    objects = models.Manager()
