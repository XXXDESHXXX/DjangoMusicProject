from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from songs.api.serializers import (
    UserSongLikeSerializer,
    UserSongLikeCreateSerializer,
    SongSerializer,
)
from songs.models import UserSongLike, Song
from utils.permissions import IsMusician, IsCurrentUserEqualsRequestUser


class SongCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsMusician)
    serializer_class = SongSerializer

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)


class SongDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserEqualsRequestUser, IsMusician)
    serializer_class = SongSerializer

    def get_object(self) -> Song:
        return get_object_or_404(Song, id=self.kwargs.get("song_id"))

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        song = self.get_object()
        self.check_object_permissions(self.request, song)
        self.perform_destroy(song)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSongLikeListAPIView(ListAPIView):
    serializer_class = UserSongLikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        song_id = self.kwargs.get('song_id')
        return UserSongLike.objects.filter(liked_song=song_id)


class UserSongLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeCreateSerializer

    def get_object(self) -> Song:
        song_id = self.request.data.get("liked_song")
        song = get_object_or_404(Song, id=song_id)
        return song

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        self.get_object()
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    "error": "IntegrityError",
                    "detail": "Bad request.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer: Serializer) -> None:
        user = self.request.user
        song = self.get_object()
        serializer.save(user=user, liked_song=song)


class UserSongLikeDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsCurrentUserEqualsRequestUser)
    serializer_class = UserSongLikeSerializer

    def get_object(self) -> UserSongLike:
        return get_object_or_404(UserSongLike, id=self.kwargs.get("song_id"))

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        user_song_like = self.get_object()
        self.check_object_permissions(self.request, user_song_like)
        self.perform_destroy(user_song_like)
        return Response(status=status.HTTP_204_NO_CONTENT)
