from itertools import chain
from typing import Any

from django.db.models import Value, CharField
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from utils import add_url_name_to_context
from constants import RATINGS

from core.custom_decorators import custom_login_required

from reviews.models import Ticket, Review
from subscriptions.models import UserFollows


class PostListsView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_lists.html'

    # @custom_login_required   # à gérer à un moment !!
    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        if url_name == 'feed':
            self.context['title'] = "Page d'accueil - Flux"

            followed_users_ids = [_user.followed_user_id
                                  for _user
                                  in UserFollows.objects.filter(user_id=request.user.id).all()]

            self.context['followed_users_posts'] = self.get_posts(followed_users_ids)

        if url_name == 'posts':
            self.context['title'] = "Mes posts"
            self.context['user_posts'] = self.get_posts([request.user.id])

        return render(request, self.template_name, {'context': self.context})

    def get_posts(self, filter_param: list[int]) -> list[Any]:
        tickets = Ticket.objects.filter(user__id__in=filter_param).all() \
            .annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.filter(user__id__in=filter_param).all() \
            .annotate(content_type=Value('REVIEW', CharField()))
        # peut surement etre amélioré !

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True)
        return posts

    #  @custom_login_required   # à gérer à un moment !!
    def post(self, request, *args, **kwargs):
        """

        """

        return render(request, self.template_name, {'context': self.context})


class PostsEditionView(TemplateView):
# faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
# PB le template n'est pas le meme ... coment faire !?
    """

    """
    context = {}
    template_name = 'reviews/posts_edition.html'

    #  @custom_login_required   # à gérer à un moment !!
    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':  # voir si je peux utiliser un dict à la place de if/elif/else
            self.context['title'] = "Créer un ticket"
        elif url_name == 'ticket_modification':
            self.context['title'] = "Modifier un ticket"
        elif url_name == 'review_creation_no_ticket':
            self.context['title'] = "Créer une critique (sans ticket préalable)"
        elif url_name == 'review_creation_reply':
            self.context['title'] = "Répondre à une demande de critique"
        elif url_name == 'review_creation_reply_specific':
            self.context['title'] = "Répondre au ticket {numero de ticket}"
        elif url_name == 'review_modification':
            self.context['title'] = "Modifier une critique"
        else:
            self.context['title'] = "DEBUG !!!???!!???"  # Debug, à retirer plus tard

        self.context['possible_ratings'] = RATINGS

        return render(request, self.template_name, {'context': self.context})

        # ticket_id = kwargs['id']

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

        if ticket_infos:
            new_ticket = Ticket(title=ticket_infos['ticket_title'], description=ticket_infos['ticket_descr'],
                                user=request.user, image=ticket_infos['ticket_image'])
            new_ticket.save()

        review_headline = request.POST.get('ticket_title')
        review_rating = request.POST.get('review_rating')
        review_comment = request.POST.get('review_comment')

        review_infos = {
            'review_headline': review_headline,
            'review_rating': review_rating,
            'review_comment': review_comment
        }

        self.context['review_infos'] = review_infos

        if review_infos:
            # imptt: ajouter "ticket= ," en premeir argument de new review
            # et trouver comment je lie au ticket correspond
            new_review = Review(headline=review_infos['review_headline'], rating=review_infos['review_rating'],
                                user=request.user, body=review_infos['review_comment'])
            new_review.save()

        return render(request, self.template_name, {'context': self.context})
