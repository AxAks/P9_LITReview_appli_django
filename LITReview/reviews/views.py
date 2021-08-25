from core.custom_decorators import custom_login_required
from django.shortcuts import render

# Create your views here.


@custom_login_required
def feed_view(request):
    return render(request, 'reviews/feed.html')

@custom_login_required
def posts_view(request):
    return render(request, 'reviews/posts.html')

@custom_login_required
def ticket_creation(request):
    return render(request, 'reviews/ticket.html')

@custom_login_required
def review_creation(request):
    return render(request, 'reviews/review.html')
