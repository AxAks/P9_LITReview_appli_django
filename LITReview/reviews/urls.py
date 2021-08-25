from django.urls import path

from .views import FeedView, PostCreation


urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('posts/', FeedView.as_view(), name='posts'),
    path('creation/ticket/', PostCreation.as_view(), name='ticket_creation'),
    path('creation/review/', PostCreation.as_view(), name='review_creation'),
]
