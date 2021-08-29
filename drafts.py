"""
## used in subscriptions/views.py

# add a user subscription to another user
new_user_followed = UserFollows(user_id=request.user.id, followed_user_id=user_to_follow.id)
new_user_followed.save()

# find a list of Objects User except current (return a queryset !!)
CustomUser.objects.filter(username__icontains=query)\
                    .distinct()\
                    .exclude(id=request.user.id)

## for reviews/views.py

# add a ticket
create_ticket = Ticket(title= , description= , user=request.user, image=  )
create_ticket .save()



title = models.CharField(max_length=128)
description = models.TextField(max_length=2048, blank=True)
user = models.ForeignKey(
    to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
image = models.ImageField(null=True, blank=True)
time_created = models.DateTimeField(auto_now_add=True)

"""