from django import forms
from core.models import CustomUser


class UserSearchForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False,
                               help_text="Cherchez le Nom d'utilisateur d'un utilisateur non suivi pour l'afficher")

    class Meta:
        model = CustomUser
        fields = ('username',)


class UserFollowForm(forms.ModelForm):
    username = forms.ModelChoiceField(queryset=CustomUser.objects.filter(username='number1fan'), required=False,
                                      help_text="A modifier")

    class Meta:
        model = CustomUser
        fields = ('username',)


class UserUnfollowForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=False,
                               help_text="A modifier")

    class Meta:
        model = CustomUser
        fields = ('username',)
