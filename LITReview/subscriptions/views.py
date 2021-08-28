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
    context = {}

    #@custom_login_required    # pb car je ne recupere pas l'user ! à voir !
    # essayer d'ajouter request.user dans custom_login_requided
    def get(self, request, *args, **kwargs):
        """
        Displays the page subscription
        """
        user_follows = UserFollows.objects.filter(user_id=request.user.id).values()
        followed_users = [CustomUser.objects.get(id=user_follows_dict['followed_user_id'])
                          for user_follows_dict in user_follows]
        return render(request, self.template_name, {'followed_users': followed_users})

    # @custom_login_required
    def post(self, request, *args, **kwargs):
        """
        Enables to search users by username and display the results as a list
        """
        form_name = request.POST.get('form_name')

        if form_name == 'search':
            query = request.POST.get('search')
            if query:
                results = CustomUser.objects.filter(username__icontains=query).distinct()
            else:
                results = []
            return render(request, self.template_name, {'results': results})

        elif form_name == 'follow':
            user_to_follow_username = request.POST.get('user_to_follow')
            user_to_follow = CustomUser.objects.get(username=user_to_follow_username)
            new_user_followed = UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)
            new_user_followed.save()
            return render(request, self.template_name, {'new_user_followed': new_user_followed})

        else:
            results = []
        return render(request, self.template_name, {'results': results})




    #@custom_login_required
    def unfollow_user(self, request) -> HttpResponse:  # à écrire
        """
        Enables to unfollow another user
        """
        query = request.POST.get('user_to_unfollow', '')
        template_name = 'subscriptions/subscriptions.html'

        return render(request, template_name)
