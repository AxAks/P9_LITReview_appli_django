from django.urls import path

from core.views import signup_view

urlpatterns = [
    path('subscriptions/', signup_view, name='subscriptions'),
    ]
