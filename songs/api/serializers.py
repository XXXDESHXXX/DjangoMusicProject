from rest_framework import serializers
from songs.models import UserSongLike


class UserSongLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSongLike
        fields = ('id', 'user', 'created_at')
