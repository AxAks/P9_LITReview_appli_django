from typing import Union

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages

from utils import add_url_name_to_context
from constants import PAGE_TITLES, RATINGS, TICKET_CREATED_MSG, TICKET_ALREADY_REPLIED_MSG, TICKET_MODIFIED_MSG,\
    TICKET_DELETED_MSG, REVIEW_CREATED_MSG, REVIEW_MODIFIED_MSG, REVIEW_DELETED_MSG, FORM_ERROR_MSG

from reviews.forms import TicketForm, ReviewForm, TicketEditForm, ReviewEditForm
from reviews.lib_reviews import get_posts, get_ticket_by_id, delete_ticket, get_review_by_id, delete_review, \
    create_ticket, edit_ticket, create_review, edit_review, get_already_replied_tickets

from subscriptions.lib_subscriptions import get_followed_users_by_id


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
        self.context = {'tickets_already_replied': []}
        url_name = add_url_name_to_context(request, self.context)
        self.context['title'] = PAGE_TITLES[url_name]

        current_user_and_followed_user_ids = []
        followed_users_ids = get_followed_users_by_id(request)
        [current_user_and_followed_user_ids.append(i) for i in followed_users_ids]
        current_user_and_followed_user_ids.append(request.user.id)

        if url_name == 'feed':
            self.template_name = 'reviews/posts_lists/my_feed.html'

        elif url_name == 'posts':
            self.template_name = 'reviews/posts_lists/my_posts.html'

        self.context['user_posts'] = get_posts([request.user.id])
        current_user_and_followed_user_posts = get_posts(current_user_and_followed_user_ids)
        self.context['current_user_and_followed_user_posts'] = current_user_and_followed_user_posts
        tickets_already_replied = get_already_replied_tickets(current_user_and_followed_user_posts)
        self.context['tickets_already_replied'] = [ticket for ticket in tickets_already_replied]

        return render(request, self.template_name, {'context': self.context})

    def post(self, request):
        """
        not used but present for the structure consistency of the project
        """
        return render(request, self.template_name, {'context': self.context})


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
            self.context['post'] = get_ticket_by_id(kwargs['id'])
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, TICKET_ALREADY_REPLIED_MSG)
                return redirect(reverse('posts'))
            else:
                self.form_ticket = TicketEditForm()

        elif url_name == 'ticket_delete':
            ticket_to_delete = get_ticket_by_id(kwargs['id'])
            self.context['post'] = ticket_to_delete
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, TICKET_ALREADY_REPLIED_MSG)
                return redirect(reverse('posts'))
            else:
                try:
                    delete_ticket(ticket_to_delete.id)
                    messages.info(request, TICKET_DELETED_MSG)
                    return redirect(reverse('posts'))
                except Exception as e:
                    raise Exception(e)

        elif url_name == 'review_ticket_reply':
            self.template_name = 'reviews/post_edition_forms/review_creation_form.html'
            self.context['post'] = get_ticket_by_id(kwargs['id'])
            self.context['replied'] = self.context['post'].review_set.exists()
            if self.context['replied']:
                messages.info(request, TICKET_ALREADY_REPLIED_MSG)
                return redirect(reverse('feed'))
            else:
                self.form_review = ReviewForm()

        elif 'review_modification' in url_name:
            self.template_name = 'reviews/post_edition_forms/review_modification_form.html'
            review_to_edit = get_review_by_id(kwargs['id'])
            self.context['post'] = review_to_edit
            self.context['associated_ticket'] = review_to_edit.ticket
            self.form_review = ReviewEditForm()

        elif url_name == 'review_delete':
            try:
                review_to_delete = get_review_by_id(kwargs['id'])
                delete_review(review_to_delete.id)
                messages.info(request, REVIEW_DELETED_MSG)
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

    def post(self, request, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Enables to:
        - create posts : Tickets and Reviews
        - Edit posts
        """
        url_name = add_url_name_to_context(request, self.context)

        if url_name == 'ticket_creation':
            try:
                create_ticket(request)
                messages.info(request, TICKET_CREATED_MSG)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/ticket_creation_form.html'
                form = TicketForm()
                messages.info(request, FORM_ERROR_MSG)
                return render(request, template_name, {'form': form})

        elif url_name == 'ticket_modification':
            try:
                ticket_to_edit = get_ticket_by_id(kwargs['id'])
                edit_ticket(request, ticket_to_edit)
                messages.info(request, TICKET_MODIFIED_MSG)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/ticket_modification_form.html'
                form = TicketEditForm()
                messages.info(request, FORM_ERROR_MSG)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_ticket_reply':
            try:
                ticket_replied_to = get_ticket_by_id(kwargs['id'])
                create_review(request, ticket_replied_to)
                messages.info(request, REVIEW_CREATED_MSG)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_creation_form.html'
                form = ReviewForm()
                messages.info(request, FORM_ERROR_MSG)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_modification':
            try:
                review_to_edit = get_review_by_id(kwargs['id'])
                edit_review(request, review_to_edit)
                messages.info(request, REVIEW_MODIFIED_MSG)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_modification_form.html'
                form = ReviewEditForm()
                messages.info(request, FORM_ERROR_MSG)
                return render(request, template_name, {'form': form})

        elif url_name == 'review_creation_no_ticket':
            try:
                ticket = create_ticket(request)
                create_review(request, ticket)
                messages.info(request, REVIEW_CREATED_MSG)
                return redirect(reverse('posts'))
            except ValidationError:
                template_name = 'reviews/post_edition_forms/review_creation_no_ticket_form.html'
                form = TicketForm()
                messages.info(request, FORM_ERROR_MSG)
                return render(request, template_name, {'form': form})
