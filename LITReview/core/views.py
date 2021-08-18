from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm #, CustomAuthenticationForm


# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('signup')
    template_name = 'registration/signup.html'


class LoginView(CreateView):
    form_class = CustomUserCreationForm  # CustomAuthenticationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'


