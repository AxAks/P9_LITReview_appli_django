from django.urls import path

from .views import subscriptions_view

urlpatterns = [
    path('', subscriptions_view, name='subscriptions'),
    ]

