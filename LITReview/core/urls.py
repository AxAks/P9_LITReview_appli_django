from django.contrib.auth.views import LoginView
from django.urls import path, include

from .views import signup_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Les dernières Views restent à écrire !!
]
