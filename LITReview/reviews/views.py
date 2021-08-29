from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView


from core.custom_decorators import custom_login_required


class FeedView(TemplateView):
    """

    """
    context = {}
    template_name = 'reviews/feed.html'

    # @custom_login_required
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # def feed_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        if request.resolver_match.url_name == 'feed':
            self.context['title'] = "Page d'accueil - Flux"
        elif request.resolver_match.url_name == 'posts':
            self.context['title'] = "Mes posts"
        else:
            self.context['title'] = "...!!???"
        return render(request, self.template_name, {'context': self.context})


    @custom_login_required
    def posts_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context['title'] = "Mes posts"
        return render(request, self.template_name, {'context': self.context})


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
