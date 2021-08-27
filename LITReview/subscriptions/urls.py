from django.urls import path

from .views import SubscriptionsView  #, follow_user, unfollow_user

urlpatterns = [
    path('', SubscriptionsView.as_view(), name='subscriptions'),
    path('', SubscriptionsView.as_view(), name='follow_user'),
    path('', SubscriptionsView.as_view(), name='unfollow_user'),
]

