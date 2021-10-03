from django import forms
from constants import RATINGS
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
    rating = forms.ChoiceField(label="Note", choices=sorted({(RATINGS[k], k) for k in RATINGS}),
                               help_text='La note de 0 à 5 que vous souhaitez donner',
                               widget=forms.widgets.RadioSelect)
    body = forms.CharField(label="Description", max_length=8192, help_text='Le corps de votre critique')

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)


class ReviewEditForm(forms.ModelForm):
    headline = forms.CharField(label="Titre", max_length=128,
                               help_text='Le titre que vous souhaitez donner à votre critique', required=False)
    rating = forms.ChoiceField(label="Note", choices=sorted({(RATINGS[k], k) for k in RATINGS}),
                               help_text='La note de 0 à 5 que vous souhaitez donner',
                               required=False, widget=forms.widgets.RadioSelect)
    body = forms.CharField(label="Description", max_length=8192, help_text='Le corps de votre critique',
                           required=False)

    class Meta:
        model = Review
        fields = ('headline', 'rating',
                  'body',)
