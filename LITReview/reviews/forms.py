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


class TicketForm(forms.ModelForm):
    title = forms.CharField(label="titre", max_length=128,
                            help_text='Le titre que vous souhaitez donner à votre Ticket')
    description = forms.CharField(label="description", max_length=2048,
                                  help_text="L'explication de votre demande")
    image = forms.ImageField(label="Ajouter une image",
                             help_text="L'illustration de votre demande: peut etre vide", required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image',)


class TicketEditForm(forms.ModelForm):
    title = forms.CharField(label="titre", max_length=128,
                            help_text='Le titre que vous souhaitez donner à votre Ticket', required=False)
    description = forms.CharField(label="description", max_length=2048,
                                  help_text="L'explication de votre demande", required=False)
    image = forms.ImageField(label="Ajouter une image",
                             help_text="L'illustration de votre demande: peut etre vide", required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image',)


class ReviewForm(forms.ModelForm):
    headline = forms.CharField(label="Titre", max_length=128,
                               help_text='Le titre que vous souhaitez donner à votre critique')
    rating = forms.IntegerField(label="Note", min_value=0, max_value=5, help_text='La note que vous souhaitez donner')
    body = forms.CharField(label="Description", max_length=8192, help_text='Le corps de votre critique')

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)


class ReviewEditForm(forms.ModelForm):
    headline = forms.CharField(label="Titre", max_length=128,
                               help_text='Le titre que vous souhaitez donner à votre critique', required=False)
    rating = forms.IntegerField(label="Note", min_value=0, max_value=5, help_text='La note que vous souhaitez donner',
                                required=False)
    body = forms.CharField(label="Description", max_length=8192, help_text='Le corps de votre critique',
                           required=False)

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)
