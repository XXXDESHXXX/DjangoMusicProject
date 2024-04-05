from django.urls import path

from lyrics.api.views import LyricSongAPIView, LyricCreateAPIView, LyricDeleteAPIView

app_name = "lyrics"

urlpatterns = [
    path("lyrics/<int:song_id>", LyricSongAPIView.as_view(), name="lyric_song_list"),
    path(
        "lyrics/create_lyric/<int:song_id>",
        LyricCreateAPIView.as_view(),
        name="create_lyric",
    ),
    path(
        "lyrics/delete_lyric/<int:lyric_id>",
        LyricDeleteAPIView.as_view(),
        name="delete_lyric",
    ),
]
