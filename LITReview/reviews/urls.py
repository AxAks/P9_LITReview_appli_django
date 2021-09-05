from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PostListsView, PostsEditionView


urlpatterns = [
    path('',
         login_required(PostListsView.as_view(), login_url='login'), name='feed'),
    path('posts/',
         login_required(PostListsView.as_view(), login_url='login'), name='posts'),
    path('ticket/creation/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='ticket_creation'),
    path('ticket/modification/<int:id>',
         login_required(PostsEditionView.as_view(), login_url='login'), name='ticket_modification'),
    path('ticket/reply/<int:id>',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_ticket_reply'),
    path('review/creation/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_creation_no_ticket'),  # pouvoir créer une review !
    path('review/modification/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_modification'),  # id review à mettre ici
]
