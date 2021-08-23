from django.shortcuts import render

# Create your views here.


def feed_view(request):
    return render(request, 'reviews/feed.html')


def posts_view(request):
    return render(request, 'reviews/posts.html')


def ticket_creation(request):
    return render(request, 'reviews/ticket_creation.html')


def review_creation(request):
    return render(request, 'reviews/review_creation.html')
