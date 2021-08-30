from django.urls import path

from .views import FeedView, PostCreation


urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('posts/', FeedView.as_view(), name='posts'),
    path('ticket/creation/', PostCreation.as_view(), name='ticket_creation'),
    path('ticket/modification/', PostCreation.as_view(), name='ticket_modification'),
    path('review/creation/', PostCreation.as_view(), name='review_creation_no_ticket'),
    path('review/reply/', PostCreation.as_view(), name='review_creation_reply'),
    path('review/modification/', PostCreation.as_view(), name='review_modification'),
]
