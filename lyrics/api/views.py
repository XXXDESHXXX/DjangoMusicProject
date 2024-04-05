from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from lyrics.models import Lyric
from lyrics.api.serializers import LyricSerializer


class LyricSongAPIView(generics.ListAPIView):
    serializer_class = LyricSerializer

    def get_queryset(self) -> Response:
        song_id = self.kwargs.get("song_id")
        return Lyric.objects.filter(song_id=song_id)


class LyricCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LyricSerializer

    def perform_create(self, serializer: Serializer) -> None:
        song_id = self.kwargs.get("song_id")

        serializer.save(song_id=song_id)

    def create(self, request: Request, *args, **kwargs) -> Lyric | Response:
        song_id = self.kwargs.get("song_id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Lyric.objects.filter(
            song_id=song_id, language=serializer.validated_data["language"]
        ):
            return Response(
                {"detail": "You cannot add the same language twice"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class LyricDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LyricSerializer

    def get_object(self) -> Lyric:
        return get_object_or_404(
            Lyric, id=self.kwargs.get("lyric_id")
        )
