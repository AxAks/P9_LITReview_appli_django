from core.custom_decorators import custom_login_required
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render

from core.models import CustomUser
from django.views.generic import TemplateView
from subscriptions.models import UserFollows


class SubscriptionsView(TemplateView):
    """
    This class manages the Subscription Page
    """
    template_name = 'subscriptions/subscriptions.html'

    #@custom_login_required    # pb car je ne recupere pas l'user ! à voir !
    def get(self, request, *args, **kwargs):
        """
        Displays the page subscription
        """
        return render(request, self.template_name)

    #@custom_login_required
    def post(self, request, *args, **kwargs):
        """
        Enables to search users by username and display the results as a list
        """
        query = request.POST.get('search', '')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).distinct()
        else:
            results = []
        return render(request, self.template_name, {'results': results})


class Subscriptions(TemplateView):
    """
    This class enables to manage subscriptions between users
    """
    template_name = 'subscriptions/subscriptions.html'

    #@custom_login_required
    def follow_user(self, request) -> HttpResponse:  # à écrire
        """
        Enables to follow another user
        """
        current_user = request.user
        user_to_follow_username = request.POST.get('user_to_follow', '')
        user_to_follow = CustomUser.objects.filter(user_to_follow_username)
        if user_to_follow:
            new_user_followed = UserFollows(user_id="current_user.id", followed_user_id=user_to_follow.user_id)
            # voir comment recupérer l'id de l'user courant  !!! (user = request.user, user_id = request.user.id)
        else:
            new_user_followed = None
        return render(request, self.template_name, {'new_user_followed': new_user_followed})

    #@custom_login_required
    def unfollow_user(self, request) -> HttpResponse:  # à écrire
        """
        Enables to unfollow another user
        """
        query = request.POST.get('user_to_unfollow', '')
        template_name = 'subscriptions/subscriptions.html'

        return render(request, template_name)
