from django.http import HttpResponse
from django.shortcuts import render

from core.models import CustomUser
from core.custom_decorators import custom_login_required


# Create your views here.


@custom_login_required
def subscriptions_view(request) -> HttpResponse:
    """

    """
    template_name = 'subscriptions/subscriptions.html'
    return render(request, template_name)


@custom_login_required
def search_user(request) -> HttpResponse:  # à écrire
    """

    """
    template_name = 'subscriptions/subscriptions.html'
    query = request.GET.get('search', '')
    if query:
        results = CustomUser.objects.filter(username__icontains=query).distinct()
    else:
        results = []
    #  user = [request if request == CustomUser.username else "Cet utilisateur n'existe pas "]
    return render(request, template_name, {'results': results})


@custom_login_required
def follow_user(request) -> HttpResponse:  # à écrire
    """

    """
    template_name = 'subscriptions/subscriptions.html'
    return render(request, template_name)


@custom_login_required
def unfollow_user(request) -> HttpResponse:  # à écrire
    """

    """
    template_name = 'subscriptions/subscriptions.html'

    return render(request, template_name)
