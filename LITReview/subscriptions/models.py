from django.db import models

from LITReview import settings


# Create your models here.

# suffisant, pas besoin d'un followed_by ? si un user follow un autre, de l'autre c^oté l'user est suivi !
class UserFollows(models.Model):
    """

    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
