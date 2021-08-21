from django.urls import path

from core.views import reviews_view

urlpatterns = [
    path('subscriptions/', reviews_view, name='subscriptions'),
    ]
