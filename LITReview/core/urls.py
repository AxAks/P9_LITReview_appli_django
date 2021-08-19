from django.contrib.auth.views import LoginView
from django.urls import path

from .views import signup_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('feed/', LoginView.as_view(template_name='feed.html'), name='feed'),
]