"""
peut etre que ce sera plus simple, et plus clair
de gerer les formualaires avec un forms.py

pour:
- creation de ticket  (avec gestion de l'envoi d'images)
- modification de ticket (avec gestion de l'envoi d'images)
- creation de review sans ticket préalable
- creation de review en réponse à un ticket
- modification de review

à voir ...
"""
from django import forms

from reviews.models import Ticket, Review


class TicketCreationForm(forms.ModelForm):
    title = forms.CharField(label="title", max_length=128, help_text='Titre')
    description = forms.CharField(label="description", max_length=2048, help_text='Description')
    image = forms.ImageField(label="image", help_text='Image')

    class Meta:
        model = Ticket
        fields = ('title', 'description',
                  'image',)

    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ticket_images', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    """


class ReviewCreationForm(forms.ModelForm):
    headline = forms.CharField(label="headline", max_length=128, help_text='Titre')
    rating = forms.IntegerField(label="rating", help_text='Note')
    body = forms.CharField(label="body", max_length=8192, help_text='Description')

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)

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
    """