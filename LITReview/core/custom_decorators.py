from django.contrib.auth.decorators import login_required


def custom_login_required(function):
    return login_required(function, login_url='login')
