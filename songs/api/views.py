from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from songs.api.serializers import UserSongLikeSerializer


class UserSongLikeCreateAPIView(CreateAPIView):
    serializer_class = UserSongLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
