from typing import Dict, Any

from rest_framework import serializers
from playlists.models import Playlist, PlaylistSong


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = (
            "id",
            "name",
            "description",
            "image",
            "created_at",
            "updated_at",
            "is_private",
        )


class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = ("id", "created_at", "song")

    def create(self, validated_data: Dict[str, Any]) -> PlaylistSong:
        return PlaylistSong.objects.create(**validated_data)
