from django.shortcuts import render

from core.models import CustomUser


# Create your views here.
def subscriptions_view(request):
    template_name = 'subscriptions/subscriptions.html'
    return render(request, template_name)


def search_user(request):  # à écrire
    template_name = 'subscriptions/subscriptions.html'
    query = request.GET.get('q', '')
    if query:
        results = CustomUser.objects.filter(name__icontains=query).distinct()
    else:
        results = []
    #  user = [request if request == CustomUser.username else "Cet utilisateur n'existe pas "]
    return render(request, template_name, {'results': results})


def follow_user(request):  # à écrire

    template_name = 'subscriptions/subscriptions.html'
    return render(request, template_name)


def unfollow_user(request):  # à écrire
    template_name = 'subscriptions/subscriptions.html'

    return render(request, template_name)
