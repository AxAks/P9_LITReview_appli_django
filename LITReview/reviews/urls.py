from django.urls import path

from core.views import reviews_view

urlpatterns = [
    path('reviews/', reviews_view, name='reviews'),
    ]
