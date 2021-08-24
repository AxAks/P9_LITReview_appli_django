from django.urls import path

from .views import subscriptions_view, search_user, follow_user, unfollow_user

urlpatterns = [
    path('', subscriptions_view, name='subscriptions'),
    path('search', search_user, name='search_user'),
    path('follow', follow_user, name='follow_user'),
    path('unfollow', unfollow_user, name='unfollow_user'),
    ]

