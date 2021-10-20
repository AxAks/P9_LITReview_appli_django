from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages

from subscriptions.forms import UserSearchForm, UserFollowForm, UserUnfollowForm
from subscriptions.lib_subscriptions import get_subscriptions_status_for_user, get_matching_users, get_specific_user, \
    unfollow_user, follow_user


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
                        }
        followed_users, following_users = get_subscriptions_status_for_user(request)
        self.context['followed_users'] = followed_users
        self.context['following_users'] = following_users

        return render(request,
                      self.template_name,
                      {'context': self.context,
                       'search_form': self.search_form,
                       'follow_form': self.follow_form,
                       'unfollow_form': self.unfollow_form
                       })

    def post(self, request):
        """
        Enables to:
        - search users by username and display the results as a list
        - follow and unfollow other users
        """
        followed_users, following_users = get_subscriptions_status_for_user(request)
        self.context['followed_users'] = followed_users
        self.context['following_users'] = following_users

        users_excluded_from_search = [user.id for user in followed_users]
        users_excluded_from_search.append(request.user.id)
        search_form = UserSearchForm(request.POST)
        follow_form = UserFollowForm(request.POST)
        unfollow_form = UserUnfollowForm(request.POST)

        if 'username' in search_form.data.keys():
            return self.search(request, users_excluded_from_search)
        elif 'follow_form' in follow_form.data.keys():
            return self.follow(request)
        elif 'unfollow_form' in unfollow_form.data.keys():
            return self.unfollow(request)

    def search(self, request, users_excluded_from_search):
        query = request.POST.get('username')
        if query:
            found_users = get_matching_users(query, users_excluded_from_search)
            self.context['found_users'] = found_users
            if found_users:
                return render(request, self.template_name, {'context': self.context, 'search_form': self.search_form})
            else:
                messages.info(request, "La recherche n'a retourné aucun utilisateur")
                return redirect(reverse('subscriptions'))
        else:
            messages.info(request, "Vous n'avez pas entré de nom d'utilisateur à rechercher")
            return redirect(reverse('subscriptions'))

    def unfollow(self, request):
        query = request.POST.get('unfollow_form')
        user_to_unfollow = get_specific_user(query)
        unfollow_user(request, user_to_unfollow)
        messages.info(request, f"L'utilisateur {query} n'est maintenant plus suivi")
        return redirect(reverse('subscriptions'))

    def follow(self, request):
        query = request.POST.get('follow_form')
        user_to_follow = get_specific_user(query)
        new_user_followed = follow_user(request, user_to_follow)
        new_user_followed.save()
        self.context['new_user_followed'] = new_user_followed.followed_user
        messages.info(request, f"L'utilisateur {query} est maintenant suivi")
        return redirect(reverse('subscriptions'))
