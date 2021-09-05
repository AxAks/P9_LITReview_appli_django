from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse

from core.models import CustomUser
from subscriptions.models import UserFollows


class SubscriptionsView(TemplateView):
    """
    This class manages the Subscription Page
    """
    template_name = 'subscriptions/subscriptions.html'
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Displays the page subscription
        taking the context into account
        """
        self.context = {'found_users': None,
                        'already_followed_user': [],
                        'not_followed_yet': [],
                        'new_user_followed': [],
                        'unfollowed_user': []
                        }

        self.get_subscriptions_status_for_user(request)

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        """
        Enables to:
        - search users by username and display the results as a list
        - follow and unfollow other users
        """
        self.get_subscriptions_status_for_user(request)
        users_excluded_from_search = [user.id for user in self.context['followed_users']]
        users_excluded_from_search.append(request.user.id)
        form_name = request.POST.get('form_name')
        if form_name == 'search':
            query = request.POST.get('searched_user')
            if query:
                found_users = CustomUser.objects.filter(username__icontains=query)\
                    .distinct()\
                    .exclude(id__in=users_excluded_from_search)
            else:
                found_users = []
            self.context['found_users'] = found_users
            return render(request, self.template_name, {'context': self.context})

        if form_name == 'follow':
            user_to_follow_username = request.POST.get('user_to_follow')
            user_to_follow = CustomUser.objects\
                .get(username=user_to_follow_username)

            new_user_followed = UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)
            new_user_followed.save()
            self.context['new_user_followed'] = new_user_followed
            return redirect(reverse('subscriptions', kwargs={}))

        elif form_name == 'unfollow':
            user_to_unfollow_username = request.POST.get('user_to_unfollow')
            user_to_unfollow = CustomUser.objects\
                .get(username=user_to_unfollow_username)
            user_unfollowed = UserFollows.objects \
                .get(user_id=request.user.id, followed_user_id=user_to_unfollow.id) \
                .delete()
            self.context['unfollowed_user'] = user_unfollowed
            return redirect(reverse('subscriptions', kwargs={}))

    def get_subscriptions_status_for_user(self, request):
        followed_users = [CustomUser.objects.get(id=relation_obj.followed_user_id)
                          for relation_obj in UserFollows.objects.filter(user_id=request.user.id).all()]
        following_users = [CustomUser.objects.get(id=user_following_obj.user_id)
                           for user_following_obj
                           in UserFollows.objects.filter(followed_user_id=request.user.id).all()]

        self.context['followed_users'] = followed_users
        self.context['following_users'] = following_users
