from typing import Union

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from constants import REGISTRATION_SUCCESS_MSG, LOGIN_SUCCESS_MSG, FORM_ERROR_MSG
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

    def post(self, request) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Handles the validation of data provided by the user in the registration form
        Leads directly to the home/feed page if the form is validated.
        Otherwise, it displays the errors and prompts to retry
        """
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username', )
            password = form.cleaned_data.get('password1', )
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, REGISTRATION_SUCCESS_MSG)
            return redirect('feed')
        else:
            messages.info(request, FORM_ERROR_MSG)
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
        """
        Displays the Login View made of two parts :
        a link to Sign Up and the Login Form
        """
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
            messages.info(request, LOGIN_SUCCESS_MSG)
            return redirect(request, self.success_to)
        else:
            messages.info(request, FORM_ERROR_MSG)
            return render(request, self.template_name, {'form': self.form})


class LogoutView(TemplateView):
    """
    Disconnects the user
    """
    template_name = 'registration/login.html'

    def get(self, request, **kwargs) -> HttpResponse:
        """
        signs the user out
        and closes his session
        """
        logout(request)
        return render(request, self.template_name)
