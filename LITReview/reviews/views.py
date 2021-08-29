from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView


from core.custom_decorators import custom_login_required


class FeedView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_lists.html'

    # @custom_login_required   # à gérer à un moment !!
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # def feed_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        url_name = request.resolver_match.url_name
        self.context['url_name'] = url_name

        if url_name == 'feed':
            self.context['title'] = "Page d'accueil - Flux"
        elif url_name == 'posts':
            self.context['title'] = "Mes posts"
        else:
            self.context['title'] = "...!!???"
        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        pass

    @custom_login_required
    def posts_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context['title'] = "Mes posts"
        return render(request, self.template_name, {'context': self.context})


class PostCreation(TemplateView):
    template_name = 'reviews/posts_edition.html'
    context = {}
    """
    
    """
    # @custom_login_required
    def get(self, request, *args, **kwargs) -> HttpResponse:
    # def ticket_creation(self, request) -> HttpResponse:
        """

        """
        url_name = request.resolver_match.url_name
        self.context['url_name'] = url_name

        # ouhlala c'est lourd ca : if, elif, elif ,elif etc ... voir si possible de rendre ca plus concis
        if request.resolver_match.url_name == 'ticket_creation':
            self.context['title'] = "Créer un ticket"
        elif request.resolver_match.url_name == 'review_creation_no_ticket':
            self.context['title'] = "Page de création de critique (sans ticket)"
        elif request.resolver_match.url_name == 'review_creation_reply':
            self.context['title'] = "Page de création de critique (en réponse à un ticket)"
        elif request.resolver_match.url_name == 'ticket_modification':
            self.context['title'] = "Page de modification d'un ticket"
        elif request.resolver_match.url_name == 'review_modification':
            self.context['title'] = "Page de modification d'une critique"
        else:
            self.context['title'] = ".heu c'est quoi là..!!???"

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        pass

    @custom_login_required
    def review_creation_no_ticket(self, request) -> HttpResponse: # à gerer dans le get
        """

        """
        return render(request, self.template_name)
