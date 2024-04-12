from django.urls import path

from lyrics.api.views import (
    LyricSongAPIView,
    LyricCreateAPIView,
    LyricDeleteAPIView,
    LyricLineTimecodeListAPIView,
    LyricLineTimecodeDeleteAPIView,
    LyricLineTimecodeCreateAPIView,
)

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
    path(
        "lyrics/<int:lyric_id>/lyric_line_timecodes",
        LyricLineTimecodeListAPIView.as_view(),
        name="lyric_line_timecode_list",
    ),
    path(
        "lyrics/delete_lyric_line_timecode/<int:lyric_line_timecode_id>",
        LyricLineTimecodeDeleteAPIView.as_view(),
        name="delete_lyric_line_timecode",
    ),
    path(
        "lyrics/create_lyric_line_timecode/<int:lyric_id>",
        LyricLineTimecodeCreateAPIView.as_view(),
        name="create_lyric_line_timecode",
    ),
]
