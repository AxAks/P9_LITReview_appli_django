from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse_lazy

from LITReview import settings


# Create your models here.
class Ticket(models.Model):
    """
    Model for a ticket
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' N°: {self.id},'\
               f' "{self.title}"'\
               f' by {self.user},'\
               f' Description: {self.description}'

    def get_absolute_url(self):
        return reverse_lazy('ticket_view', kwargs={'post_id': self.id})

    objects = models.Manager()


class Review(models.Model):
    """
    Model for a Review
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' Ticket: {self.ticket.title},'\
               f' Title: {self.headline},'\
               f' Reply by: {self.user},'\
               f' Description: {self.body}'

    objects = models.Manager()

