from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages

from core.models import CustomUser
from subscriptions.forms import UserSearchForm, UserFollowForm, UserUnfollowForm
from subscriptions.models import UserFollows


class SubscriptionsView(TemplateView):
    """
    This class manages the Subscription Page
    """
    template_name = 'subscriptions/my_subscriptions.html'
    context = {}
    search_form = UserSearchForm()
    follow_form = UserFollowForm()
    unfollow_form = UserUnfollowForm()

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

        return render(request,
                      self.template_name,
                      {'context': self.context,
                       'search_form': self.search_form,
                       'follow_form': self.follow_form,
                       'unfollow_form': self.unfollow_form
                       })

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
        search_form = UserSearchForm(request.POST)
        follow_form = UserFollowForm(request.POST)
        unfollow_form = UserUnfollowForm(request.POST)

        if form_name is None and search_form['username'] != '':
            return self.search(request, users_excluded_from_search)
        elif form_name is None and follow_form['username'] != '':
            return self.follow(request)
        elif form_name is None and unfollow_form['username'] != '':
            return self.unfollow(request)

    def search(self, request, users_excluded_from_search):
        query = request.POST.get('username')
        if query:
            found_users = CustomUser.objects.filter(username__icontains=query) \
                .distinct() \
                .exclude(id__in=users_excluded_from_search)
            self.context['found_users'] = found_users
            if found_users:
                return render(request, self.template_name, {'context': self.context, 'search_form': self.search_form})
            else:
                messages.info(request, "La recherche n'a retourné aucun utilisateur")
                return redirect(reverse('subscriptions'))

    def unfollow(self, request):
        query = request.POST.get('username')
        user_to_unfollow = CustomUser.objects \
            .get(username=query)
        user_unfollowed = UserFollows.objects \
            .get(user_id=request.user.id, followed_user_id=user_to_unfollow.id) \
            .delete()
        self.context['unfollowed_user'] = user_unfollowed
        messages.info(request, f"L'utilisateur {query} n'est maintenant plus suivi")
        return render(request, self.template_name, {'context': self.context, 'unfollow_form': self.unfollow_form})
        return redirect(reverse('subscriptions'))

    def follow(self, request):
        query = request.POST.get('username')
        user_to_follow = CustomUser.objects \
            .get(username=query)
        new_user_followed = UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)
        new_user_followed.save()
        self.context['new_user_followed'] = new_user_followed
        messages.info(request, f"L'utilisateur {query} est maintenant suivi")
        return render(request, self.template_name, {'context': self.context, 'follow_form': self.follow_form})
        return redirect(reverse('subscriptions', kwargs={}))

    def get_subscriptions_status_for_user(self, request):
        followed_users = [CustomUser.objects.get(id=relation_obj.followed_user_id)
                          for relation_obj in UserFollows.objects.filter(user_id=request.user.id).all()]
        following_users = [CustomUser.objects.get(id=user_following_obj.user_id)
                           for user_following_obj
                           in UserFollows.objects.filter(followed_user_id=request.user.id).all()]

        self.context['followed_users'] = followed_users
        self.context['following_users'] = following_users
