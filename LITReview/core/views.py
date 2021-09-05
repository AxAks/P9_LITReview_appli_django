from typing import Union

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import SignUpForm


class SignupView(TemplateView):
    """

    """
    template_name = 'registration/signup.html'

    def signup_view(self, request) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Handles the signup form
        Lads directly to the home/feed page if the form is validated.
        """
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('feed')
        else:
            form = SignUpForm()
            print("errors detected, FIND HOW TO display these errors for retry, validators work"
                  "BUT no error display and retry (find validation rules and edit if needed + enable to retry")
            # si trop long à debugger, pour trouver la solution, ne pas perdre de temps dessus, je le ferai à la fin !
            # plutot se concentrer sur les fonctionnalités à développer
            return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    """

    """
    success_to = 'feed'
    failure_redirect = 'login'

    def login_view(self, request) -> HttpResponseRedirect:
        """
        Logs the user in after validating the provided login information
        """
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            login(request, user)
            return redirect(request, self.success_to)
        else:
            return redirect(request, self.failure_redirect)


class LogoutView(TemplateView):
    """

    """
    template_name = 'registration/login.html'

    def logout_view(self, request) -> HttpResponseRedirect:
        """
        signs the user out
        and closes his session
        """
        logout(request)
        return render(request, self.template_name)
