from itertools import chain
from typing import Any

from django.db.models import Value, CharField
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from utils import add_url_name_to_context
from constants import RATINGS

from reviews.models import Ticket, Review
from subscriptions.models import UserFollows

from constants import PAGE_TITLES


class PostListsView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts"
    """

    """
    context = {}
    template_name = 'reviews/posts_lists.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]

        if url_name == 'feed':
            followed_users_ids = [_user.followed_user_id
                                  for _user
                                  in UserFollows.objects.filter(user_id=request.user.id).all()]
            self.context['followed_users_posts'] = self.get_posts(followed_users_ids)

        elif url_name == 'posts':
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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]
        self.context['possible_ratings'] = RATINGS

        if url_name in ('ticket_modification', 'review_ticket_reply'):
            ticket_id = kwargs['id']
            self.context['post'] = Ticket.objects.get(id=ticket_id)

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        """

        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':
            # new ticket creation
            ticket_title = request.POST.get('ticket_title')
            ticket_description = request.POST.get('ticket_description')
            ticket_image = request.POST.get('ticket_image') if request.POST.get('ticket_image') else None

            ticket_infos = {
                'ticket_title': ticket_title,
                'ticket_description': ticket_description,
                'ticket_image': ticket_image
            }

            self.context['ticket_infos'] = ticket_infos

            new_ticket = Ticket(title=ticket_infos['ticket_title'], description=ticket_infos['ticket_description'],
                                user=request.user, image=ticket_infos['ticket_image'])
            new_ticket.save()

            return redirect(reverse('posts'))
            # peut etre à rediriger autre part plus tard une page "ticket_created", à voir

        elif url_name == 'review_creation_no_ticket':
            #  new review creation
            review_headline = request.POST.get('review_headline')
            review_rating = request.POST.get('review_rating')
            review_comment = request.POST.get('review_comment')

            review_infos = {
                'review_headline': review_headline,
                'review_rating': review_rating,
                'review_comment': review_comment
            }

            self.context['review_infos'] = review_infos

            #  imptt: ajouter "ticket= ," en premier argument de new review
            # et trouver comment je lie au ticket correspond (cré en meme temps)
            new_review = Review(headline=review_infos['review_headline'], rating=review_infos['review_rating'],
                                user=request.user, body=review_infos['review_comment'])
            new_review.save()

        elif url_name == 'ticket_modification':
            #  ticket modification
            new_ticket_title = request.POST.get('new_ticket_title')
            new_ticket_description = request.POST.get('new_ticket_description')
            new_ticket_image = request.POST.get('new_ticket_image')

            updated_ticket_infos = {
                'new_ticket_title':  new_ticket_title if new_ticket_title else ticket_title,
                'new_ticket_description': new_ticket_description if new_ticket_description else ticket_description,
                'new_ticket_image': new_ticket_image if new_ticket_image else ticket_image
            }
            if updated_ticket_infos['new_ticket_title']:
                self.context['post'].update(title=updated_ticket_infos['new_ticket_title'])
            if updated_ticket_infos['new_ticket_description']:
                self.context['post'].update(description=updated_ticket_infos['new_ticket_description'])
            if updated_ticket_infos['new_ticket_image']:
                self.context['post'].update(image=updated_ticket_infos['new_ticket_description'])

        elif url_name == 'review_ticket_reply':
            ticket_to_reply_id = kwargs['id']
            ticket_to_reply = Ticket.objects.get(id=ticket_to_reply_id)

            #  new review creation
            review_headline = request.POST.get('review_headline')
            review_rating = request.POST.get('review_rating')
            review_comment = request.POST.get('review_comment')

            review_infos = {
                'review_headline': review_headline,
                'review_rating': review_rating,
                'review_comment': review_comment
            }

            self.context['review_infos'] = review_infos

            if review_infos:
                new_review = Review(ticket=ticket_to_reply, headline=review_infos['review_headline'],
                                    rating=review_infos['review_rating'], user=request.user,
                                    body=review_infos['review_comment'])
                new_review.save()

            return render(request, self.template_name, {'context': self.context})

