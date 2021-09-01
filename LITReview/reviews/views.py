from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from core.custom_decorators import custom_login_required

from reviews.models import Ticket
from subscriptions.models import UserFollows
from core.models import CustomUser


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
        self.context = {}
        url_name = self.add_url_name_to_context(request)

        if url_name == 'feed':
            self.context['title'] = "Page d'accueil - Flux"

            users = [_user.followed_user_id for _user in UserFollows.objects.filter(user_id=request.user.id).all()]
            following_users_posts = Ticket.objects.filter(user__id__in=users).all()
            # peut surement etre amélioré !


            self.context['following_users_posts'] = following_users_posts

        if url_name == 'posts':
            self.context['title'] = "Mes posts"

            user_posts_query = Ticket.objects.filter(user_id=request.user.id).values()    # ajouter les reviews aussi plus tard
            user_posts = [Ticket.objects.get(user_id=user_posts_dict['user_id'])
                                             for user_posts_dict in user_posts_query]
            self.context['user_posts'] = user_posts

        return render(request, self.template_name, {'context': self.context})

    #  @custom_login_required   # à gérer à un moment !!
    def post(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name, {'context': self.context})

    def add_url_name_to_context(self, request):
        self.context['url_name'] = request.resolver_match.url_name
        return self.context['url_name']


class PostsEditionView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_edition.html'

    #  @custom_login_required   # à gérer à un moment !!
    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
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

    #  @custom_login_required   # à gérer à un moment !!
    def post(self, request, *args, **kwargs):
        """

        """
        ticket_title = request.POST.get('ticket_title')
        ticket_descr = request.POST.get('ticket_descr')
        ticket_image = request.POST.get('ticket_image') if request.POST.get('ticket_image') else None

        ticket_infos = {
            'ticket_title': ticket_title,
            'ticket_descr': ticket_descr,
            'ticket_image': ticket_image
        }

        self.context['ticket_infos'] = ticket_infos

        new_ticket = Ticket(title=ticket_infos['ticket_title'], description=ticket_infos['ticket_descr'],
                            user=request.user, image=ticket_infos['ticket_image'])
        new_ticket.save()

        return render(request, self.template_name, {'context': self.context})

    def add_url_name_to_context(self, request):
        self.context['url_name'] = request.resolver_match.url_name
        return self.context['url_name']
