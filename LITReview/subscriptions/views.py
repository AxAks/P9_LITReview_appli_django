from django.shortcuts import render

# Create your views here.


def subscriptions_view(request):
    return render(request, 'subscriptions/subscriptions.html')


