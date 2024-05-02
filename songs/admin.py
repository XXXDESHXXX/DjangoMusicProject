from django.contrib import admin
from .models import Song, UserSongLike


@admin.register(UserSongLike)
class UserSongLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "liked_song")
    list_filter = ("created_at",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "genre", "user")
    exclude = ("likes",)
