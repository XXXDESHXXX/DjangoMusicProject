from django.contrib import admin
from .models import User, UserFollow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('description', 'role', 'image', 'is_private')
    list_filter = ('is_private', 'role')
