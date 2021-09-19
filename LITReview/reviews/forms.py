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
    title = forms.CharField(label="titre", max_length=128, help_text='Titre')
    description = forms.CharField(label="description", max_length=2048, help_text='Description')
    image = forms.ImageField(label="image", help_text='Image', required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description',
                  'image',)


class ReviewCreationForm(forms.ModelForm):
    headline = forms.CharField(label="titre", max_length=128, help_text='Titre')
    rating = forms.IntegerField(label="note", help_text='Note')
    body = forms.CharField(label="description", max_length=8192, help_text='Description')

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)
