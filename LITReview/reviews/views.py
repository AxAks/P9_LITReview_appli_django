from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView


from core.custom_decorators import custom_login_required


class PostListsView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_lists.html'

    # @custom_login_required   # à gérer à un moment !!
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # def feed_view(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        url_name = self.add_url_name_to_context(request)

        if url_name == 'feed':
            self.context['title'] = "Page d'accueil - Flux"
        elif url_name == 'posts':
            self.context['title'] = "Mes posts"

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        pass

    def add_url_name_to_context(self, request):
        self.context['url_name'] = request.resolver_match.url_name
        return self.context['url_name']


class PostsEditionView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_edition.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:

        url_name = self.add_url_name_to_context(request)

        if url_name == 'ticket_creation':
            self.context['title'] = "Créer un ticket"
        elif url_name == 'review_creation_no_ticket':
            self.context['title'] = "Créer une critique (sans ticket)"
        elif url_name == 'review_creation_reply':
            self.context['title'] = "Répondre à une demande de critique"
        elif url_name == 'ticket_modification':
            self.context['title'] = "Modifier un ticket"
        elif url_name == 'review_modification':
            self.context['title'] = "Modifier une critique"
        else:
            self.context['title'] = ".heu on est où là..!!???"

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        pass

    def add_url_name_to_context(self, request):
        self.context['url_name'] = request.resolver_match.url_name
        return self.context['url_name']
