from django.urls import path

from lyrics.api.views import LyricSongAPIView

app_name = "lyrics"

urlpatterns = [
    path("lyrics/<int:song_id>", LyricSongAPIView.as_view(), name="lyric_song"),
]
