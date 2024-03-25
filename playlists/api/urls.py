from django.urls import path

from playlists.api.views import PlaylistListAPIView, UserPlaylistListAPIView, PlaylistCreateAPIView, \
    PlaylistDeleteAPIView, PlaylistUpdateAPIView, PlaylistSongCreateAPIView, PlaylistSongDeleteAPIView

app_name = "playlists"

urlpatterns = [
    path("playlists/", PlaylistListAPIView.as_view(), name="list_of_playlists"),
    path("user/<int:user_id>/playlists/",
         UserPlaylistListAPIView.as_view(),
         name="user_playlist_list"),
    path("playlists/create/",
         PlaylistCreateAPIView.as_view(),
         name="playlist_create"),
    path("playlists/delete/<int:playlist_id>",
         PlaylistDeleteAPIView.as_view(),
         name="playlist_delete"),
    path("playlists/update/<int:playlist_id>",
         PlaylistUpdateAPIView.as_view(),
         name="playlist_update"),
    path("playlists/<int:playlist_id>/create_playlist_song",
         PlaylistSongCreateAPIView.as_view(),
         name="create_playlist_song"),
    path("playlists/<int:playlist_id>/delete_playlist_song",
         PlaylistSongDeleteAPIView.as_view(),
         name="delete_playlist_song"),
]
