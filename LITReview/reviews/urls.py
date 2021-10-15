from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PostListsView, PostsEditionView


urlpatterns = [
    path('feed/',
         login_required(PostListsView.as_view(), login_url='login'), name='feed'),
    path('posts/',
         login_required(PostListsView.as_view(), login_url='login'), name='posts'),
    path('ticket/creation/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='ticket_creation'),
    path('ticket/modification/<int:id>',
         login_required(PostsEditionView.as_view(), login_url='login'), name='ticket_modification'),
    path('ticket/delete/<int:id>',
         login_required(PostsEditionView.as_view(), login_url='login'), name='ticket_delete'),
    path('ticket/reply/<int:id>/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_ticket_reply'),
    path('review/creation/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_creation_no_ticket'),
    path('review/modification/<int:id>/',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_modification'),
    path('review/delete/<int:id>',
         login_required(PostsEditionView.as_view(), login_url='login'), name='review_delete'),
]
