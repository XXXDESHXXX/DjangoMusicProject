from rest_framework import generics
from rest_framework.response import Response

from lyrics.models import Lyric
from lyrics.api.serializers import LyricSerializer


class LyricSongAPIView(generics.ListAPIView):
    serializer_class = LyricSerializer

    def get_queryset(self) -> Response:
        song_id = self.kwargs.get("song_id")
        return Lyric.objects.filter(song_id=song_id)
