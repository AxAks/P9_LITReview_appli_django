from django.contrib.auth.views import LoginView
from django.urls import path, include

from .views import signup_view, logout_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
