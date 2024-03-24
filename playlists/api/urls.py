from django.urls import path

from playlists.api.views import PlaylistListAPIView, UserPlaylistListAPIView, PlaylistCreateAPIView

app_name = "playlists"

urlpatterns = [
    path("playlists/", PlaylistListAPIView.as_view(), name="list_of_playlists"),
    path("user/<int:user_id>/playlists/",
         UserPlaylistListAPIView.as_view(),
         name="user_playlist_list"),
    path("playlists/create/",
         PlaylistCreateAPIView.as_view(),
         name="playlist_create")
]
