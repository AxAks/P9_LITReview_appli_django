from itertools import chain
from typing import Any, Union, List

from django.core.exceptions import ValidationError
from django.db.models import Value, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages

import constants
from reviews.forms import TicketForm, ReviewForm, TicketEditForm, ReviewEditForm
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
        self.context = {'ticket_already_replied': []}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]

        if url_name == 'feed':
            current_user_and_followed_user_ids = []
            followed_users_ids = self.get_followed_users_by_id(request)
            [current_user_and_followed_user_ids.append(i) for i in followed_users_ids]
            current_user_and_followed_user_ids.append(request.user.id)
            self.template_name = 'reviews/posts_lists/my_feed.html'
            self.context['current_user_and_followed_user_posts'] = self.get_posts(current_user_and_followed_user_ids)
            self.check_replied_tickets(self.context['current_user_and_followed_user_posts'])

        elif url_name == 'posts':
            self.template_name = 'reviews/posts_lists/my_posts.html'
            self.context['user_posts'] = self.get_posts([request.user.id])
            self.check_replied_tickets(self.context['user_posts'])

        return render(request, self.template_name, {'context': self.context})

    def check_replied_tickets(self, posts):
        for post in posts:
            if post.content_type == 'TICKET':
                if post.review_set.exists():
                    self.context['ticket_already_replied'].append(
                        post)
            elif post.content_type == 'REVIEW':
                if post.ticket:
                    self.context['ticket_already_replied'].append(post)

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
    def get_posts(cls, filter_param: List[int]) -> List[Any]:
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
            self.template_name = 'reviews/post_edition_forms/ticket_creation_form.html'
            self.form_ticket = TicketForm()

        elif url_name == 'ticket_modification':
            self.template_name = 'reviews/post_edition_forms/ticket_modification_form.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id']) # voir pourquoi il attend un Review ici !
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, constants.ticket_already_replied)
                return redirect(reverse('posts'))
                #  voir comment utiliser self.context['post'].review_set pour verifier si le ticket a une/des reviews
            else:
                self.form_ticket = TicketEditForm()

        elif url_name == 'ticket_delete':
            ticket_to_delete = self.get_ticket_by_id(kwargs['id'])
            self.context['post'] = ticket_to_delete
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, constants.ticket_already_replied)
                return redirect(reverse('posts'))
            else:
                try:
                    self.delete_ticket(ticket_to_delete.id)
                    messages.info(request, constants.ticket_deleted)
                    return redirect(reverse('posts'))
                except Exception as e:
                    raise Exception(e)

        elif url_name == 'review_ticket_reply':
            self.template_name = 'reviews/post_edition_forms/review_creation_form.html'
            self.context['post'] = self.get_ticket_by_id(kwargs['id'])
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, constants.ticket_already_replied)
                return redirect(reverse('feed'))
            else:
                self.form_review = ReviewForm()

        elif 'review_modification' in url_name:
            self.template_name = 'reviews/post_edition_forms/review_modification_form.html'
            review_to_edit = self.get_review_by_id(kwargs['id'])
            self.context['post'] = review_to_edit
            self.context['associated_ticket'] = review_to_edit.ticket
            self.form_review = ReviewEditForm()

        elif url_name == 'review_delete':
            try:
                review_to_delete = self.get_review_by_id(kwargs['id'])
                self.delete_review(review_to_delete.id)
                messages.info(request, constants.review_deleted)
                return redirect(reverse('posts'))
            except Exception as e:
                raise Exception(e)

        elif url_name == 'review_creation_no_ticket':
            self.template_name = 'reviews/post_edition_forms/review_creation_no_ticket_form.html'
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
                messages.info(request, constants.ticket_created)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/ticket_creation_form.html'
                form = TicketForm()
                messages.info(request, constants.form_error)
                return render(request, template_name, {'form': form})

        elif url_name == 'ticket_modification':
            try:
                ticket_to_edit = self.get_ticket_by_id(kwargs['id'])
                self.edit_ticket(request, ticket_to_edit)
                messages.info(request, constants.ticket_modified)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/ticket_modification_form.html'
                form = TicketEditForm()
                messages.info(request, constants.form_error)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_ticket_reply':
            try:
                ticket_replied_to = self.get_ticket_by_id(kwargs['id'])
                self.create_review(request, ticket_replied_to)
                messages.info(request, constants.review_created)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_creation_form.html'
                form = ReviewForm()
                messages.info(request, constants.form_error)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_modification':
            try:
                review_to_edit = self.get_review_by_id(kwargs['id'])
                self.edit_review(request, review_to_edit)
                messages.info(request, constants.review_modified)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_modification_form.html'
                form = ReviewEditForm()
                messages.info(request, constants.form_error)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_creation_no_ticket':
            try:
                ticket = self.create_ticket(request)
                self.create_review(request, ticket)
                messages.info(request, constants.review_created)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_creation_no_ticket_form.html'
                form = TicketForm()
                messages.info(request, constants.form_error)
                return render(request, template_name, {'form': form})

    @classmethod
    def create_ticket(cls, request) -> Ticket:
        """
        Enable to create and save a ticket (a request for a review)
        """
        form = TicketForm(request.POST or None, request.FILES or None)
        try:
            form.is_valid()
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return ticket
        except ValidationError as e:
            raise ValidationError(e)

    @classmethod
    def edit_ticket(cls, request, ticket_to_edit: Ticket) -> Ticket:
        """
        Enable to modify an already registered Ticket
        If one fields remains empty, the previous value is kept
        """

        edited_request_post = request.POST.copy()
        edited_request_files = request.FILES.copy()

        if request.POST['title'] == '':
            edited_request_post['title'] = ticket_to_edit.title
        else:
            edited_request_post['title'] = request.POST['title']
        if request.POST['description'] == '':
            edited_request_post['description'] = ticket_to_edit.description
        else:
            edited_request_post['description'] = request.POST['description']

        # gestion des images à faire correctement !
        # actuellement je peux remplacer une image mais pas enlever une image d'un ticket
        # + pb sauvegarde du fichier en double avec extension bizarre à un moment...
        if ticket_to_edit.image != '' \
                and 'image' not in request.FILES.keys() \
                and request.POST['image'] == '':
            edited_request_post['image'] = ticket_to_edit.image

        elif ticket_to_edit.image == '' \
                and 'image' in request.FILES.keys() \
                and 'image' not in request.POST.keys():
            edited_request_files['image'] = request.FILES['image']

        elif 'image' not in request.FILES.keys() \
                and request.POST['image'] == '':
            edited_request_post = request.POST['image']

        elif 'image' in request.FILES.keys() \
                and 'image' not in request.POST.keys():
            edited_request_post = ''

        form = TicketEditForm(edited_request_post or None, edited_request_files or None, instance=ticket_to_edit)
        try:
            form.is_valid()
            form.save()
            return ticket_to_edit
        except ValidationError as e:
            raise ValidationError(e)

    @classmethod
    def delete_ticket(cls, ticket_id) -> None:
        """
        Enables to delete a given Ticket
        """
        return Ticket.objects.filter(pk=ticket_id).delete()

    @classmethod
    def create_review(cls, request, ticket_replied_to: Ticket) -> Review:
        """
        Enables to create a review (a response to a Ticket)
        """
        form = ReviewForm(request.POST)
        try:
            form.is_valid()
            review = form.save(commit=False)
            review.ticket, review.user = ticket_replied_to, request.user
            review.save()
            return review
        except Exception as e:
            raise ValidationError(e)

    @classmethod
    def edit_review(cls, request, review_to_edit: Review) -> Review:
        """
        Enables to modify an already registered Review
        If one fields remains empty, the previous value is kept
        """
        edited_request_post = request.POST.copy()

        if request.POST['headline'] == '':
            edited_request_post['headline'] = review_to_edit.headline
        else:
            edited_request_post['headline'] = request.POST['headline']
        if request.POST['rating'] == '':
            edited_request_post['rating'] = review_to_edit.rating
        else:
            edited_request_post['rating'] = request.POST['rating']
        if request.POST['body'] == '':
            edited_request_post['body'] = review_to_edit.body
        else:
            edited_request_post['body'] = request.POST['body']

        form = ReviewEditForm(edited_request_post, instance=review_to_edit)
        try:
            form.is_valid()
            form.save()
            return review_to_edit
        except Exception as e:
            raise ValidationError(e)

    @classmethod
    def delete_review(cls, review_id) -> None:
        """
        Enables to delete a given Review
        """
        return Review.objects.filter(pk=review_id).delete()

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
