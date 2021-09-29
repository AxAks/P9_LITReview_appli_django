from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ticket, Review

admin.site.register(Ticket)
admin.site.register(Review)
