from rest_framework import serializers
from songs.models import UserSongLike


class UserSongLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSongLike
        fields = ('id', 'user', 'liked_song', 'created_at')
        read_only_fields = ('created',)


class UserSongLikeCreateSerializer(UserSongLikeSerializer):
    class Meta(UserSongLikeSerializer.Meta):
        read_only_fields = UserSongLikeSerializer.Meta.read_only_fields + ('user',)
