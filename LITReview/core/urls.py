from django.contrib.auth.views import LoginView
from django.urls import path

from .views import signup_view, feed_view, subscriptions_view, reviews_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('feed/', feed_view, name='feed'),
    path('subscriptions/', subscriptions_view, name='subscriptions'),
    path('reviews/', reviews_view, name='subscriptions')
    # Les 3 dernières Views restent à écrire !!
]
