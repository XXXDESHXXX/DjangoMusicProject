from django.contrib import admin
from .models import Playlist, PlaylistSong


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "created_at", "is_private", "description", "user")
    list_filter = ("created_at", "updated_at", "is_private")
    search_fields = ("name", "description")


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ("created_at", "song")
    list_filter = ("created_at",)
