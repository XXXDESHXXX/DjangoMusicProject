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
    path("song/<int:song_id>/", LyricSongAPIView.as_view(), name="lyric_song_list"),
    path(
        "create/<int:song_id>/",
        LyricCreateAPIView.as_view(),
        name="create_lyric",
    ),
    path(
        "delete/<int:lyric_id>/",
        LyricDeleteAPIView.as_view(),
        name="delete_lyric",
    ),
    path(
        "lyric_line_timecodes/<int:lyric_id>/",
        LyricLineTimecodeListAPIView.as_view(),
        name="lyric_line_timecode_list",
    ),
    path(
        "lyric_line_timecode/delete/<int:lyric_line_timecode_id>/",
        LyricLineTimecodeDeleteAPIView.as_view(),
        name="delete_lyric_line_timecode",
    ),
    path(
        "lyric_line_timecode/create/<int:lyric_id>/",
        LyricLineTimecodeCreateAPIView.as_view(),
        name="create_lyric_line_timecode",
    ),
]
