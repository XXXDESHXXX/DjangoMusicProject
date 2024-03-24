from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from playlists.models import Playlist
from .serializers import PlaylistSerializer


class PlaylistListAPIView(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class UserPlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Playlist.objects.filter(user_id=user_id)


class PlaylistCreateAPIView(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
