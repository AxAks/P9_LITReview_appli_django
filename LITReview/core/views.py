from typing import Union

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages

import constants
from .forms import SignUpForm


class SignupView(TemplateView):
    """
    Manages the user's registration
    """
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Displays an empty registration form
        """
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Handles the validation of data provided by the user in the registration form
        Leads directly to the home/feed page if the form is validated.
        Otherwise, it displays the errors and prompts to retry
        """
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, constants.registration_success)
            return redirect('feed')
        else:
            messages.info(request, constants.form_error)
            return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    """
    Manages the user's authentication
    """
    template_name = 'registration/login.html'
    form = AuthenticationForm()
    success_to = 'feed'
    failure_redirect = 'login'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, {'form': self.form})

    def post(self, request) -> HttpResponseRedirect:
        """
        Logs the user in after validating the provided login information
        """
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            login(request, user)
            messages.info(request, constants.login_success)
            return redirect(request, self.success_to)
        else:
            messages.info(request, constants.form_error)
            return render(request, self.template_name, {'form': self.form})


class LogoutView(TemplateView):
    """

    """
    template_name = 'registration/login.html'

    def get(self, request) -> HttpResponse:
        """
        signs the user out
        and closes his session
        """
        logout(request)
        return render(request, self.template_name)
