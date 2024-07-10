from rest_framework import serializers
from songs.models import UserSongLike
from songs.models import Song
from songs.validators import validate_song_file


class UserSongLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSongLike
        fields = ("id", "user", "liked_song", "created_at")
        read_only_fields = ("created",)


class UserSongLikeCreateSerializer(UserSongLikeSerializer):
    class Meta(UserSongLikeSerializer.Meta):
        read_only_fields = UserSongLikeSerializer.Meta.read_only_fields + ("user",)


class SongSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_song_file])

    class Meta:
        model = Song
        fields = ("id", "name", "file", "likes", "genre", "user")
