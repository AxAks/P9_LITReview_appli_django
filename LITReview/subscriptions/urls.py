from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import SubscriptionsView  #, follow_user, unfollow_user

urlpatterns = [
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='subscriptions'),
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='follow_user'),
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='unfollow_user'),
]

