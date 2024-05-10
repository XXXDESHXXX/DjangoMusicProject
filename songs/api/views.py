from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from songs.models import Song

from songs.api.serializers import (
    UserSongLikeSerializer,
    UserSongLikeCreateSerializer,
    SongSerializer,
)
from songs.models import UserSongLike, Song
from utils.permissions import IsMusician


class SongCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsMusician)
    serializer_class = SongSerializer

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)


class SongDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsMusician)
    serializer_class = SongSerializer

    def get_object(self) -> Song:
        song = get_object_or_404(Song, id=self.kwargs.get("song_id"))
        if song.user != self.request.user:
            raise PermissionDenied("You do not have permission for this action.")
        return song


class UserSongLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeCreateSerializer

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
