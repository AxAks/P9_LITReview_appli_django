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

        users_following = UserFollows.objects.filter(followed_user_id=request.user.id).values()
        following_users = [CustomUser.objects.get(id=user_following_dict['user_id'])
                           for user_following_dict in users_following]

        self.context['followed_users'] = followed_users
        self.context['following_users'] = following_users

        return render(request, self.template_name, {'context': self.context})

    # @custom_login_required
    def post(self, request, *args, **kwargs):
        """
        Enables to search users by username and display the results as a list
        """
        form_name = request.POST.get('form_name')

        if form_name == 'search':
            query = request.POST.get('searched_user')
            if query:
                found_users = CustomUser.objects.filter(username__icontains=query)\
                    .distinct()\
                    .exclude(id=request.user.id)
            else:
                found_users = []
            self.context['found_users'] = found_users

        if form_name == 'follow':
            user_to_follow_username = request.POST.get('user_to_follow')
            user_to_follow = CustomUser.objects\
                .get(username=user_to_follow_username)
            new_user_followed = UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)
            new_user_followed.save()
            self.context['new_user_followed'] = new_user_followed

        if form_name == 'unfollow':
            user_to_unfollow_username = request.POST.get('user_to_unfollow')
            user_to_unfollow = CustomUser.objects\
                .get(username=user_to_unfollow_username)
            user_unfollowed = UserFollows.objects\
                .get(user_id=request.user.id, followed_user_id=user_to_unfollow.id)\
                .delete()
            self.context['unfollowed_user'] = user_unfollowed

        return render(request, self.template_name, {'context': self.context})


    #@custom_login_required
    def unfollow_user(self, request) -> HttpResponse:  # à écrire
        """
        Enables to unfollow another user
        """
        query = request.POST.get('user_to_unfollow', '')
        template_name = 'subscriptions/subscriptions.html'

        return render(request, template_name)
