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

    # @custom_login_required    # pb car je ne recupere pas l'user ! à voir !
    def get(self, request, *args, **kwargs):
        """
        Displays the page subscription
        """
        followed_users = CustomUser.objects.all().select_related('userfollows').filter(id=2)
            #UserFollows.objects.filter(user_id=request.user.id).select_related('user').get()

        followed_users_usernames = followed_users.username
        return render(request, self.template_name, {'followed_users_usernames': followed_users_usernames})

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
            current_user = request.user
            user_to_follow_username = request.POST.get('user_to_follow')
            user_to_follow = CustomUser.objects.get(username=user_to_follow_username)
            new_user_followed = UserFollows(user_id=current_user.id, followed_user_id=user_to_follow.id)
            new_user_followed.save()
            return render(request, self.template_name, {'new_user_followed': new_user_followed})

        else:
            results = []
        return render(request, self.template_name, {'results': results})


    #@custom_login_required
    def follow_user(self, request) -> HttpResponse:  # à écrire
        current_user = request.user
        user_to_follow_username = request.POST.get('form_follow', '')
        user_to_follow = CustomUser.objects.filter(user_to_follow_username)
        if user_to_follow:
            new_user_followed = UserFollows(user_id=current_user.id, followed_user_id=user_to_follow.user_id)
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
