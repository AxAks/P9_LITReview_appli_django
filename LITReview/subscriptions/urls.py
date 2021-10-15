from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import SubscriptionsView

urlpatterns = [
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='subscriptions'),
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='follow_user'),
    path('', login_required(SubscriptionsView.as_view(), login_url='login'), name='unfollow_user'),
]
