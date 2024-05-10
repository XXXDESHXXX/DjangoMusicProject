from django.urls import path

from songs.api.views import (
    UserSongLikeCreateAPIView,
    UserSongLikeDeleteAPIView,
    SongCreateAPIView, SongDeleteAPIView,
)

app_name = "songs"

urlpatterns = [
    path("songs/create", SongCreateAPIView.as_view(), name="create_song"),
    path("songs/delete/<int:song_id>", SongDeleteAPIView.as_view(), name="delete_song"),
    path(
        "songs/likes/create/",
        UserSongLikeCreateAPIView.as_view(),
        name="user_like_create",
    ),
    path(
        "songs/likes/delete/<int:song_id>",
        UserSongLikeDeleteAPIView.as_view(),
        name="user_like_delete",
    ),
]
