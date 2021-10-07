from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', max_length=100, help_text='Prénom')
    last_name = forms.CharField(label='Nom', max_length=100, help_text='Nom')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)
