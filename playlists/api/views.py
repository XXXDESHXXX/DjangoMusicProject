from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from playlists.models import Playlist
from .serializers import PlaylistSerializer


class PlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()


class UserPlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self) -> Response:
        user_id = self.kwargs['user_id']
        return Playlist.objects.filter(user_id=user_id)


class PlaylistCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)


class PlaylistDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaylistSerializer

    def get_object(self) -> Playlist:
        return get_object_or_404(Playlist,
                                 user=self.request.user,
                                 id=self.kwargs.get("playlist_id")
                                 )
