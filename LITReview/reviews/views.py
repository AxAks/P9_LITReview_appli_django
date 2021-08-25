from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from core.custom_decorators import custom_login_required


class FeedView(TemplateView):
    """

    """
    template_name = 'reviews/feed.html'

    @custom_login_required
    def feed_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        return render(request, self.template_name)


    @custom_login_required
    def posts_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        return render(request, self.template_name)


class PostCreation(TemplateView):
    template_name = 'reviews/review.html'
    """

    """
    @custom_login_required
    def ticket_creation(self, request) -> HttpResponse:
        """

        """
        return render(request, self.template_name)


    @custom_login_required
    def review_creation(self, request) -> HttpResponse:
        """

        """
        return render(request, self.template_name)
