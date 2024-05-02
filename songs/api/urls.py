from django.urls import path

from songs.api.views import (
    UserSongLikeCreateAPIView,
    UserSongLikeDeleteAPIView,
    SongListAPIView, SongCreateAPIView,
)

app_name = "songs"

urlpatterns = [
    path("songs/", SongListAPIView.as_view(), name="song_list"),
    path("songs/create", SongCreateAPIView.as_view(), name="create_song"),
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
