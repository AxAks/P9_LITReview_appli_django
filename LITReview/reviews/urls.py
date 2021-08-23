from django.urls import path

from .views import posts_view, feed_view, ticket_creation, review_creation


urlpatterns = [
    path('', feed_view, name='feed'),
    path('posts/', posts_view, name=' posts'),
    path('creation/ticket/', ticket_creation, name='ticket_creation'),
    path('creation/review/', review_creation, name='review_creation'),

    ]
