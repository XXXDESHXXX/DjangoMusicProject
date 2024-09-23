from django.urls import path

from songs.api.views import (
    UserSongLikeCreateAPIView,
    UserSongLikeDeleteAPIView,
    SongCreateAPIView,
    SongDeleteAPIView, UserSongLikeListAPIView,
)

app_name = "songs"

urlpatterns = [
    path("create/", SongCreateAPIView.as_view(), name="create_song"),
    path("delete/<int:song_id>/", SongDeleteAPIView.as_view(), name="delete_song"),
    path(
        "likes/create/",
        UserSongLikeCreateAPIView.as_view(),
        name="user_like_create",
    ),
    path(
        "likes/delete/<int:song_id>/",
        UserSongLikeDeleteAPIView.as_view(),
        name="user_like_delete",
    ),
    path('song/<int:song_id>/likes/', UserSongLikeListAPIView.as_view(), name='song-likes'),
]
