from itertools import chain
from typing import Any

from django.db.models import Value, CharField
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from reviews.forms import TicketForm, ReviewForm
from utils import add_url_name_to_context
from constants import PAGE_TITLES, RATINGS

from reviews.models import Ticket, Review
from subscriptions.models import UserFollows


class PostListsView(TemplateView):  #  faire une seule classe au final ! (fusionner, factoriser tout ce qui est "posts")
    """
    Manages the pages for post lists(Tickets and Reviews)
    using the context to choose what to display:
    - Feed: other users posts
    - Posts:User's posts
    """
    context = {}
    template_name = ''

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """

        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]

        if url_name == 'feed':
            followed_users_ids = self.get_followed_users_by_id(request)
            self.template_name = 'reviews/posts_lists/my_feed.html'
            self.context['followed_users_posts'] = self.get_posts(followed_users_ids)

        elif url_name == 'posts':
            self.template_name = 'reviews/posts_lists/my_posts.html'
            self.context['user_posts'] = self.get_posts([request.user.id])

        return render(request, self.template_name, {'context': self.context})

    def post(self, request, *args, **kwargs):  # pas utilisé !
        """

        """
        return render(request, self.template_name, {'context': self.context})

    @classmethod
    def get_followed_users_by_id(cls, request) -> list[int]:
        """
        Enables to get the IDs for users followed by the current user
        """
        followed_users_ids = [_user.followed_user_id
                              for _user
                              in UserFollows.objects.filter(user_id=request.user.id).all()]
        return followed_users_ids

    @classmethod
    def get_posts(cls, filter_param: list[int]) -> list[Any]:
        """
        Enables to concatenate Tickets and Reviews under the variable name: Posts
        for the users given as parameter
        """
        tickets = Ticket.objects.filter(user__id__in=filter_param).all() \
            .annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.filter(user__id__in=filter_param).all() \
            .annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True)
        return posts


class PostsEditionView(TemplateView):
    #  faire une seule classe au final ? (fusionner, factoriser tout ce qui est "posts"
    # PB le template n'est pas le meme ... comment faire !? voir plus tard si je le fais
    """
    Manages the pages for post edition (Tickets and Reviews)
    """
    template_name = ''
    form = None
    context = {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Displays the pages for post creation, edition (Tickets and Reviews)
        using the context to choose what to display:
        """
        self.context = {}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]
        self.context['possible_ratings'] = RATINGS

        if url_name == 'ticket_creation':
            self.template_name = 'reviews/post_edition/ticket_creation.html'
            self.form = TicketForm()

        elif url_name == 'ticket_modification':
            self.template_name = 'reviews/post_edition/ticket_modification.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id'])
            self.form = TicketForm()

        elif url_name == 'review_ticket_reply':
            self.template_name = 'reviews/post_edition/review_creation.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id'])
            self.form = ReviewForm()

        elif url_name == 'review_creation_no_ticket':
            self.template_name = 'reviews/post_edition/review_creation_no_ticket.html'
            self.form = ReviewForm()  # pb on a pas le form pour le ticket pour le moment

        elif 'review_modification' in url_name:
            self.template_name = 'reviews/post_edition/review_modification.html'
            review_to_edit = self.get_review_by_id(kwargs['id'])
            self.context['post'] = review_to_edit
            associated_ticket_id = review_to_edit.ticket.id
            self.context['associated_ticket'] = self.get_ticket_by_id(associated_ticket_id)

        return render(request, self.template_name, {'form': self.form, 'context': self.context})

    def post(self, request, *args, **kwargs):
        """
        Enables to:
        - create posts : Tickets and Reviews
        - Edit posts
        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':
            return self.create_ticket(request)

        elif url_name == 'ticket_modification':
            ticket_to_edit = self.get_ticket_by_id(kwargs['id'])
            return self.edit_ticket(request, ticket_to_edit)

        elif url_name == 'review_ticket_reply':
            ticket_replied_to = self.get_ticket_by_id(kwargs['id'])
            return self.create_review(request, ticket_replied_to)

        # à compléter (coté template: validation via le bouton de validation des reviews,
        # ne prend pas en compte les champs de création de ticket !)
        elif url_name == 'review_creation_no_ticket':
            ticket = self.create_ticket(request)
            self.create_review(request, ticket)
            return redirect(
                reverse('posts'))

        elif url_name == 'review_modification':
            specific_review = self.get_review_by_id(kwargs['id'])
            self.edit_review(request, specific_review)
            return redirect(
                reverse('posts'))

    @classmethod
    def create_ticket(cls, request) -> Ticket:
        """
        Enable to create and save a ticket (a request for a review)
        """
        template_name = 'reviews/post_edition/ticket_creation.html'
        form = TicketForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(
                reverse('posts'))
        else:
            form = TicketForm()
            return render(request, template_name, {'form': form})

    @classmethod
    def edit_ticket(cls, request, ticket_to_edit: Ticket) -> Ticket:
        """
        Enable to modify an already registered Ticket
        """
        template_name = 'reviews/post_edition/ticket_modification.html'
        form = TicketForm(request.POST or None, request.FILES or None, instance=ticket_to_edit)
        if form.is_valid():
            ticket_to_edit = form.save(commit=False)
            ticket_to_edit.user = request.user
            ticket_to_edit.save()
            return redirect(
                reverse('posts'))
        else:
            form = TicketForm()
            return render(request, template_name, {'form': form})

    @classmethod
    def create_review(cls, request, ticket_replied_to: Ticket) -> Review:
        """
        Enables to create a review (a response to a Ticket)
        """
        template_name = 'reviews/post_edition/review_creation.html'
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket, review.user = ticket_replied_to, request.user
            review.save()
            return redirect(
                reverse('posts'))
        else:
            form = ReviewForm()
            return render(request, template_name, {'form': form})

    @classmethod
    def edit_review(cls, request, review: Review) -> Review:
        """
        Enables to modify an already registered Review
        """
        review_new_headline = request.POST.get('review_new_headline')
        review_new_rating = request.POST.get('review_new_rating')
        review_new_comment = request.POST.get('review_new_comment')
        if review_new_headline is not None:
            Review.objects.filter(id=review.id).update(headline=review_new_headline)
        if review_new_rating is not None:
            Review.objects.filter(id=review.id).update(rating=review_new_rating)
        if review_new_comment is not None:
            Review.objects.filter(id=review.id).update(body=review_new_comment)
        updated_review = Review.objects.get(id=review.id)
        return updated_review

    @classmethod
    def get_review_by_id(cls, review_id) -> Review:
        """
        Enbales to get a given Review by its ID
        """
        return Review.objects.get(id=review_id)

    @classmethod
    def get_ticket_by_id(cls, ticket_id) -> Ticket:
        """
        Enbales to get a given Ticket by its ID
        """
        return Ticket.objects.get(pk=ticket_id)
