from django.contrib.auth import authenticate, login, logout
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
        return redirect('feed')
    else:
        form = SignUpForm()
        print("errors detected, FIND HOW TO display these errors for retry, validators work"
              "BUT no error display and retry (find validation rules and edit if needed + enable to retry")
        # si trop long à debugger, pour trouver la solution, ne pas perdre de temps dessus, je le ferai à la fin !
        # plutot se concentrer sur les fonctionnalités à développer
        return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'reviews/feed.html')
    else:
        return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'registration/login.html')
