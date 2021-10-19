"""
Collection of functions related to the subscriptions views/classes (POST and GET):
- SubscriptionsView
"""
from core.models import CustomUser
from subscriptions.models import UserFollows


def get_followed_users_by_id(request) -> list[int]:
    """
    Enables to get the IDs for users followed by the current user
    """
    followed_users_ids = [_user.followed_user_id
                          for _user
                          in UserFollows.objects.filter(user_id=request.user.id).all()]
    return followed_users_ids


def get_subscriptions_status_for_user(request):
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
