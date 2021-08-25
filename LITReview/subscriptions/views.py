from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from core.models import CustomUser
from core.custom_decorators import custom_login_required


# Create your views here.


class SubscriptionsView(View):
    template_name = 'subscriptions/subscriptions.html'

    # @custom_login_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    # @custom_login_required
    def post(self, request, *args, **kwargs):
        query = request.POST.get('search', '')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).distinct()
        else:
            results = []
        return render(request, self.template_name, {'results': results})


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
