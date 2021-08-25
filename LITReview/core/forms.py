from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):  # est ce que j'en ai vraiment besoin ? j'ai SignUpForm !

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):  # pas utilisé (encore)!

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Prénom')
    last_name = forms.CharField(max_length=100, help_text='Nom')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)
        """
        field_classes = {
                            'username': UsernameField
                            'first_name': FirstNameField
                            'last_name': LastNameField
                            'email': EmailField
                         }
        """
