from django.urls import path

from playlists.api.views import PlaylistListAPIView, UserPlaylistListAPIView, PlaylistCreateAPIView, \
    PlaylistDeleteAPIView, PlaylistUpdateAPIView, PlaylistSongCreateAPIView

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
    path("playlists/<int:playlist_id>/add_song",
         PlaylistSongCreateAPIView.as_view(),
         name="add_song")
]
