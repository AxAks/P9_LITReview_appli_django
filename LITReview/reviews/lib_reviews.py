"""
Collection of functions related to the reviews views/classes (POST and GET):
- PostListsView
- PostsEditionView
"""
from itertools import chain
from typing import List, Union

from django.core.exceptions import ValidationError
from django.db.models import Value, CharField

from reviews.forms import ReviewEditForm, ReviewForm, TicketEditForm, TicketForm
from reviews.models import Ticket, Review


def get_posts(filter_param: List[int]) -> List[Union[Ticket, Review]]:
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


def get_already_replied_tickets(posts: List[Union[Ticket]]) -> List[Ticket]:
    """
    Enables to filter replied tickets in a given list of tickets
    """
    tickets_already_replied = []
    for post in posts:
        if post.content_type == 'TICKET':
            if post.review_set.exists():
                tickets_already_replied.append(post)
        elif post.content_type == 'REVIEW':
            if post.ticket:
                tickets_already_replied.append(post.ticket)
    return tickets_already_replied


def create_ticket(request) -> Ticket:
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


def edit_ticket(request, ticket_to_edit: Ticket) -> Ticket:
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

    if ticket_to_edit.image != '' \
            and 'image' not in request.FILES.keys() \
            and request.POST['image'] == '':
        edited_request_post['image'] = ticket_to_edit.image

    elif ticket_to_edit.image == '' \
            and 'image' in request.FILES.keys() \
            and 'image' not in request.POST.keys():
        edited_request_files['image'] = request.FILES['image']

    elif ticket_to_edit.image == '' \
            and 'image' not in request.FILES.keys() \
            and request.POST['image'] == '':
        edited_request_files['image'] = request.POST['image']

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


def delete_ticket(ticket_id: int) -> None:
    """
    Enables to delete a given Ticket
    """
    return Ticket.objects.filter(pk=ticket_id).delete()


def create_review(request, ticket_replied_to: Ticket) -> Review:
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


def edit_review(request, review_to_edit: Review) -> Review:
    """
    Enables to modify an already registered Review
    If one fields remains empty, the previous value is kept
    """
    edited_request_post = request.POST.copy()

    if request.POST['headline'] == '':
        edited_request_post['headline'] = review_to_edit.headline
    else:
        edited_request_post['headline'] = request.POST['headline']
    if 'rating' not in request.POST.keys():
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


def delete_review(review_id: int) -> None:
    """
    Enables to delete a given Review
    """
    return Review.objects.filter(pk=review_id).delete()


def get_review_by_id(review_id: int) -> Review:
    """
    Enables to get a given Review by its ID
    """
    return Review.objects.get(pk=review_id)


def get_ticket_by_id(ticket_id: int) -> Ticket:
    """
    Enables to get a given Ticket by its ID
    """
    return Ticket.objects.get(pk=ticket_id)
