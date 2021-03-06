"""
Collection of functions related to the subscriptions views/classes (POST and GET):
- SubscriptionsView
"""
from typing import List, Tuple

from core.models import CustomUser
from subscriptions.models import UserFollows


def follow_user(request, user_to_follow):
    return UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)


def unfollow_user(request, user_to_unfollow: CustomUser) -> None:
    return UserFollows.objects\
        .get(user_id=request.user.id, followed_user_id=user_to_unfollow.id)\
        .delete()


def get_specific_user(query: str) -> CustomUser:
    """
    Returns the User with the exact matching username
    """
    return CustomUser.objects.get(username=query)


def get_matching_users(query: str, users_excluded_from_search: List[int]) -> List[CustomUser]:
    """
    Returns a list of users whose usernames matched the query
    """
    return CustomUser.objects.filter(username__icontains=query)\
        .distinct()\
        .exclude(id__in=users_excluded_from_search)


def get_followed_users_by_id(request) -> list[int]:
    """
    Enables to get the IDs for users followed by the current user
    """
    followed_users_ids = [_user.followed_user_id
                          for _user
                          in UserFollows.objects.filter(user_id=request.user.id).all()]
    return followed_users_ids


def get_subscriptions_status_for_user(request) -> Tuple[List[CustomUser], List[CustomUser]]:
    """
    Returns two lists from the current user's ID:
    - The users following the current user
    - The users followed by the current user
    """
    followed_users = [CustomUser.objects.get(id=relation_obj.followed_user_id)
                      for relation_obj in UserFollows.objects.filter(user_id=request.user.id).all()]
    following_users = [CustomUser.objects.get(id=user_following_obj.user_id)
                       for user_following_obj
                       in UserFollows.objects.filter(followed_user_id=request.user.id).all()]
    return followed_users, following_users
