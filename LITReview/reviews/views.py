from itertools import chain
from typing import Any, Union

from django.db.models import Value, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from reviews.forms import TicketForm, ReviewForm
from utils import add_url_name_to_context
from constants import PAGE_TITLES, RATINGS

from reviews.models import Ticket, Review
from subscriptions.models import UserFollows


class PostListsView(TemplateView):
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
    """
    Manages the pages for post edition (Tickets and Reviews)
    """
    template_name = ''
    context = {}
    form = None
    form_ticket = None
    form_review = None

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
            self.form_ticket = TicketForm()

        elif url_name == 'ticket_modification':
            self.template_name = 'reviews/post_edition/ticket_modification.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id']) # voir pourquoi il attend un Review ici !
            self.form_ticket = TicketForm()

        elif url_name == 'review_ticket_reply':
            self.template_name = 'reviews/post_edition/review_creation.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id'])
            self.form_review = ReviewForm()

        elif 'review_modification' in url_name:
            self.template_name = 'reviews/post_edition/review_modification.html'
            review_to_edit = self.get_review_by_id(kwargs['id'])
            self.context['post'] = review_to_edit
            self.form_review = ReviewForm()

        elif url_name == 'review_creation_no_ticket':
            self.template_name = 'reviews/post_edition/review_creation_no_ticket.html'
            self.form_ticket = TicketForm()
            self.form_review = ReviewForm()

        return render(request, self.template_name, {'form_ticket': self.form_ticket if self.form_ticket else None,
                                                    'form_review': self.form_review if self.form_review else None,
                                                    'context': self.context})

    def post(self, request, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Enables to:
        - create posts : Tickets and Reviews
        - Edit posts
        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':
            try:
                self.create_ticket(request)
                return redirect(reverse('posts'))
            except Exception:  #  voir pour faire un FormException plus specifique
                template_name = 'reviews/post_edition/ticket_creation.html'
                form = TicketForm()
                return render(request, template_name, {'form': form})

        elif url_name == 'ticket_modification':
            # empecher de modifier une critique si il y a deja une reponse !
            # autoriser le fait de ne pas etre obligé de changer tous les champs du formulaire:
                # laisser l'ancienne valeur du champs si il est vide dans le nouveau formulaire
            try:
                ticket_to_edit = self.get_ticket_by_id(kwargs['id'])
                self.edit_ticket(request, ticket_to_edit)
                return redirect(reverse('posts'))
            except Exception:  #  voir pour faire un FormException plus specifique
                template_name = 'reviews/post_edition/ticket_modification.html'
                form = TicketForm()
                return render(request, template_name, {'form': form})

        elif url_name == 'review_ticket_reply':
            # empecher de créer une critique si il existe deja une critique pour le ticket
            try:
                ticket_replied_to = self.get_ticket_by_id(kwargs['id'])
                self.create_review(request, ticket_replied_to)
                return redirect(reverse('posts'))
            except Exception: #  voir pour faire un FormException plus specifique
                template_name = 'reviews/post_edition/review_creation.html'
                form = ReviewForm()
                return render(request, template_name, {'form': form})

        elif url_name == 'review_modification':
            # autoriser le fait de ne pas etre obligé de changer tous les champs du formulaire:
                # laisser l'ancienne valeur du champs si il est vide dans le nouveau formulaire
            try:
                review_to_edit = self.get_review_by_id(kwargs['id'])
                self.edit_review(request, review_to_edit)
                return redirect(reverse('posts'))
            except Exception:  #   voir pour faire un FormException plus specifique
                template_name = 'reviews/post_edition/review_modification.html'
                form = ReviewForm()
                return render(request, template_name, {'form': form})

        elif url_name == 'review_creation_no_ticket':
            try:
                ticket = self.create_ticket(request)
                self.create_review(request, ticket)
                return redirect(reverse('posts'))
            except Exception:  # voir pour faire un FormException plus specifique
                template_name = 'reviews/post_edition/review_creation_no_ticket.html'
                form = TicketForm()
                return render(request, template_name, {'form': form})

    @classmethod
    def create_ticket(cls, request) -> Ticket:
        """
        Enable to create and save a ticket (a request for a review)
        """
        form = TicketForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return ticket
        else:
            raise Exception()

    @classmethod
    def edit_ticket(cls, request, ticket_to_edit: Ticket) -> Ticket:
        """
        Enable to modify an already registered Ticket
        """
        form = TicketForm(request.POST or None, request.FILES or None, instance=ticket_to_edit)
        if form.is_valid():
            form.save()
            return ticket_to_edit
        else:
            raise Exception()

    @classmethod
    def create_review(cls, request, ticket_replied_to: Ticket) -> Review:
        """
        Enables to create a review (a response to a Ticket)
        """
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket, review.user = ticket_replied_to, request.user
            review.save()
            return review
        else:
            raise Exception()

    @classmethod
    def edit_review(cls, request, review_to_edit: Review) -> Review:
        """
        Enables to modify an already registered Review
        """
        form = ReviewForm(request.POST, instance=review_to_edit)
        if form.is_valid():
            form.save()
            return review_to_edit
        else:
            raise Exception()

    @classmethod
    def get_review_by_id(cls, review_id) -> Review:
        """
        Enables to get a given Review by its ID
        """
        return Review.objects.get(pk=review_id)

    @classmethod
    def get_ticket_by_id(cls, ticket_id) -> Ticket:
        """
        Enables to get a given Ticket by its ID
        """
        return Ticket.objects.get(pk=ticket_id)
