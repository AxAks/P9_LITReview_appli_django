from django.urls import path

from .views import FeedView, PostsEditionView


urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('posts/', FeedView.as_view(), name='posts'),
    path('ticket/creation/', PostsEditionView.as_view(), name='ticket_creation'),
    path('ticket/modification/', PostsEditionView.as_view(), name='ticket_modification'),
    path('review/creation/', PostsEditionView.as_view(), name='review_creation_no_ticket'),
    path('review/reply/', PostsEditionView.as_view(), name='review_creation_reply'),
    path('review/modification/', PostsEditionView.as_view(), name='review_modification'),
]
