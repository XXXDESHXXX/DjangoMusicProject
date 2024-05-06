from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
