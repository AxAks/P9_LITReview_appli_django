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
    Displays the pages for post lists(Tickets and Reviews)
    using the context to choose what to display:
    - Feed: other users posts
    - Posts:User's posts
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
        Displays the pages for post creation, edition (Tickets and Reviews)
        using the context to choose what to display:
        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]
        self.context['possible_ratings'] = RATINGS

        if url_name in ('ticket_modification', 'review_ticket_reply'):
            self.context['post'] = self.get_ticket_by_id(kwargs)


        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):
        """
        Enables to:
        - create posts : Tickets and Reviews
        - Edit posts
        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':
            self.create_ticket(request)
            return redirect(reverse('posts'))  # peut etre à rediriger autre part plus tard une page "ticket_created", à voir

        elif url_name == 'review_ticket_reply':
            specific_ticket = self.get_ticket_by_id(**kwargs)
            self.create_review(request, specific_ticket)  # new review creation
            return redirect(reverse('posts'))  #  peut etre à rediriger autre part plus tard une page "review_created", à voir

        elif url_name == 'review_creation_no_ticket':  # à compléter (coté template: validation via le bouton de validation des reviews, ne prend pas en compte les champs de création de ticket !)
            ticket = self.create_ticket(request)  # new ticket creation
            self.create_review(request, ticket)  #  new review creation
            return redirect(reverse('posts'))  #  peut etre à rediriger autre part plus tard une page "review_created", à voir

        elif url_name == 'ticket_modification':
            specific_ticket = self.get_ticket_by_id(kwargs)
            #  ticket modification
            new_ticket_title = request.POST.get('new_ticket_title')
            new_ticket_description = request.POST.get('new_ticket_description')
            new_ticket_image = request.POST.get('new_ticket_image')

            if new_ticket_title is not None:
                Ticket.objects.filter(id=specific_ticket.id).update(title=new_ticket_title)
            if new_ticket_description is not None:
                Ticket.objects.filter(id=specific_ticket.id).update(description=new_ticket_description)
            if new_ticket_image is not None:
                Ticket.objects.filter(id=specific_ticket.id).update(image=new_ticket_image)

            return redirect(reverse('posts'))
            # peut etre à rediriger autre part plus tard une page "ticket_created", à voir

    def get_ticket_by_id(self, kwargs):
        ticket_id = kwargs['id']
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket

    def create_ticket(self, request):
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
        return new_ticket

    def create_review(self, request, ticket):
        review_headline = request.POST.get('review_headline')
        review_rating = request.POST.get('review_rating')
        review_comment = request.POST.get('review_comment')

        review_infos = {
            'review_headline': review_headline,
            'review_rating': review_rating,
            'review_comment': review_comment
        }

        self.context['review_infos'] = review_infos
        new_review = Review(ticket=ticket, headline=review_infos['review_headline'], rating=review_infos['review_rating'],
                            user=request.user, body=review_infos['review_comment'])
        new_review.save()
        return new_review
