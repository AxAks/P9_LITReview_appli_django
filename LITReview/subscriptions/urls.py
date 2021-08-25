from django.urls import path

from .views import SubscriptionsView, follow_user, unfollow_user

urlpatterns = [
    path('', SubscriptionsView.as_view(), name='subscriptions'),
    path('follow', follow_user, name='follow_user'),
    path('unfollow', unfollow_user, name='unfollow_user'),
    ]

