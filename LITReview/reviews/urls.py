from django.urls import path

from .views import PostListsView, PostsEditionView


urlpatterns = [
    path('', PostListsView.as_view(), name='feed'),
    path('posts/', PostListsView.as_view(), name='posts'),
    path('ticket/creation/', PostsEditionView.as_view(), name='ticket_creation'),
    path('ticket/modification/<int:id>', PostsEditionView.as_view(), name='ticket_modification'),
    path('ticket/reply/<int:id>', PostsEditionView.as_view(), name='review_ticket_reply'),
    path('review/creation/', PostsEditionView.as_view(), name='review_creation_no_ticket'),  # pouvoir créer une review !
    path('review/modification/', PostsEditionView.as_view(), name='review_modification'),  # id review à mettre ici
]
