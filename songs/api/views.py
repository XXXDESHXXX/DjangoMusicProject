from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from songs.api.serializers import (
    UserSongLikeSerializer,
    UserSongLikeCreateSerializer,
    SongSerializer,
)
from songs.models import UserSongLike, Song


class UserSongLikeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeCreateSerializer

    def perform_create(self, serializer: Serializer) -> None:
        user = self.request.user

        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if UserSongLike.objects.filter(
            user=user, liked_song=serializer.validated_data["liked_song"]
        ):
            return Response(
                {"detail": "You cannot like the same song twice"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class UserSongLikeDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSongLikeSerializer

    def get_object(self) -> UserSongLike:
        song_id = self.kwargs.get("song_id")
        user = self.request.user
        song = get_object_or_404(Song, id=song_id)
        return get_object_or_404(UserSongLike, user=user, liked_song=song)


class SongListAPIView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
