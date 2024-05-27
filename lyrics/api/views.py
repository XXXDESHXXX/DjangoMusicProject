from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from lyrics.models import Lyric, LyricLineTimecode
from lyrics.api.serializers import LyricSerializer, LyricLineTimecodeSerializer
from lyrics.paginators import LyricLineTimecodePageLimitOffsetPagination
from songs.models import Song
from utils.permissions import IsMusician, IsCurrentUserEqualsRequestUser


class LyricSongAPIView(generics.ListAPIView):
    serializer_class = LyricSerializer

    def get_queryset(self) -> QuerySet:
        song_id = self.kwargs.get("song_id")
        return Lyric.objects.filter(song_id=song_id)


class LyricCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserEqualsRequestUser, IsMusician)
    serializer_class = LyricSerializer

    def get_object(self) -> Song:
        song_id = self.kwargs.get("song_id")
        song = get_object_or_404(Song, id=song_id)
        self.check_object_permissions(self.request, song)
        return song

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    "error": "IntegrityError",
                    "detail": "This combination of language and song already exists.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(song=self.get_object())


class LyricDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserEqualsRequestUser, IsMusician)
    serializer_class = LyricSerializer

    def get_object(self) -> Lyric:
        return get_object_or_404(Lyric, id=self.kwargs.get("lyric_id"))

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        instance = self.get_object()
        song = instance.song
        self.check_object_permissions(self.request, song)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LyricLineTimecodeListAPIView(generics.ListAPIView):
    serializer_class = LyricLineTimecodeSerializer
    pagination_class = LyricLineTimecodePageLimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        lyric_id = self.kwargs.get("lyric_id")
        return LyricLineTimecode.objects.filter(lyric_id=lyric_id)


class LyricLineTimecodeDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserEqualsRequestUser, IsMusician)
    serializer_class = LyricLineTimecodeSerializer

    def get_object(self) -> LyricLineTimecode:
        return get_object_or_404(
            LyricLineTimecode, id=self.kwargs.get("lyric_line_timecode_id")
        )

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        instance = self.get_object()
        lyric = instance.lyric
        self.check_object_permissions(self.request, lyric.song)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LyricLineTimecodeCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsMusician)
    serializer_class = LyricLineTimecodeSerializer

    def perform_create(self, serializer: Serializer) -> None:
        lyric_id = self.kwargs.get("lyric_id")

        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)

        lyric = Lyric.objects.get(id=lyric_id)

        if lyric.song.user != self.request.user:
            raise PermissionDenied("You do not have sufficient rights for this action")

        serializer.save(
            lyric_id=lyric_id,
        )
