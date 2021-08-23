from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import SignUpForm


# Create your views here.

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('login')
    else:
        form = SignUpForm()
        print("errors detected, FIND HOW TO display these errors for retry, validators work"
              "BUT no error display and retry (find validation rules and edit if needed + enable to retry")
        # si trop long à debugger, pour trouver la solution, ne pas perdre de temps dessus, je le ferai à la fin !
        # plutot se concentrer sur les fonctionnalités à développer
    return render(request, 'registration/signup.html', {'form': form})


def feed_view(request):
    return render(request, 'feed.html')


def subscriptions_view(request):
    return render(request, 'subscriptions.html')


def reviews_view(request):
    return render(request, 'review_creation.html')
