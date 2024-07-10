from django.urls import path

from playlists.api.views import (
    UserPlaylistListAPIView,
    PlaylistCreateAPIView,
    PlaylistDeleteAPIView,
    PlaylistUpdateAPIView,
    PlaylistSongCreateAPIView,
    PlaylistSongDeleteAPIView,
    UserPlaylistSongListAPIView,
)

app_name = "playlists"

urlpatterns = [
    path(
        "user/<int:user_id>/",
        UserPlaylistListAPIView.as_view(),
        name="user_playlist_list",
    ),
    path(
        "user/playlist_songs/<int:playlist_id>/",
        UserPlaylistSongListAPIView.as_view(),
        name="user_playlist_song_list",
    ),
    path("create/", PlaylistCreateAPIView.as_view(), name="playlist_create"),
    path(
        "delete/<int:playlist_id>/",
        PlaylistDeleteAPIView.as_view(),
        name="playlist_delete",
    ),
    path(
        "update/<int:playlist_id>/",
        PlaylistUpdateAPIView.as_view(),
        name="playlist_update",
    ),
    path(
        "create_playlist_song/<int:playlist_id>/",
        PlaylistSongCreateAPIView.as_view(),
        name="create_playlist_song",
    ),
    path(
        "delete_playlist_song/<int:playlist_song_id>/",
        PlaylistSongDeleteAPIView.as_view(),
        name="delete_playlist_song",
    ),
]
