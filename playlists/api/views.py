from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from playlists.models import Playlist, PlaylistSong
from .serializers import PlaylistSerializer, PlaylistSongSerializer
from ..paginators import UserPlaylistPageLimitOffsetPagination


class UserPlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    pagination_class = UserPlaylistPageLimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        user_id = self.kwargs.get("user_id")

        if self.request.user.id != user_id:
            return Playlist.objects.filter(is_private=False, user_id=user_id)
        return Playlist.objects.filter(user_id=user_id)


class PlaylistCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)


class PlaylistDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def get_object(self) -> Playlist:
        return get_object_or_404(
            Playlist, user=self.request.user, id=self.kwargs.get("playlist_id")
        )


class PlaylistUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def get_object(self) -> Playlist:
        return get_object_or_404(
            Playlist, user=self.request.user, id=self.kwargs.get("playlist_id")
        )


class PlaylistSongCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSongSerializer

    def perform_create(self, serializer: Serializer) -> None:
        playlist = get_object_or_404(Playlist, id=self.kwargs.get("playlist_id"))
        if playlist.user != self.request.user:
            raise PermissionDenied("You do not have permission for this action.")

        serializer.save(playlist=playlist)


class PlaylistSongDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSongSerializer

    def get_object(self) -> PlaylistSong:
        playlist_song = get_object_or_404(
            PlaylistSong, id=self.kwargs.get("playlist_song_id")
        )

        if playlist_song.playlist.user != self.request.user:
            raise PermissionDenied("You do not have permission for this action.")

        return playlist_song
