from django.http import HttpResponse
from django.shortcuts import render

from core.custom_decorators import custom_login_required

# Create your views here.


@custom_login_required
def feed_view(request) -> HttpResponse:
    """

    """
    return render(request, 'reviews/feed.html')


@custom_login_required
def posts_view(request) -> HttpResponse:
    """

    """
    return render(request, 'reviews/posts.html')


@custom_login_required
def ticket_creation(request) -> HttpResponse:
    """

    """
    return render(request, 'reviews/ticket.html')


@custom_login_required
def review_creation(request) -> HttpResponse:
    """

    """
    return render(request, 'reviews/review.html')
