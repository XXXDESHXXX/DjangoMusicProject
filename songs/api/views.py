from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
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


class UserSongLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeCreateSerializer

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        liked_song_id = self.request.data.get("liked_song")
        if not Song.objects.filter(id=liked_song_id).exists():
            return Response({"Error": "Bad Request"})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: Serializer) -> None:
        user = self.request.user

        serializer.save(user=user)


class UserSongLikeDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeSerializer

    def get_object(self) -> UserSongLike:
        song_id = self.kwargs.get("song_id")
        user = self.request.user
        song = get_object_or_404(Song, id=song_id)
        return get_object_or_404(UserSongLike, user=user, liked_song=song)
