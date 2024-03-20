from django.contrib import admin
from .models import User, UserFollow


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to", "created")
    list_filter = ("created",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "role", "image", "is_private")
    list_filter = ("is_private", "role")
