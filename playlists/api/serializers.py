from rest_framework import serializers
from playlists.models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'image', 'created_at', 'updated_at', 'is_private', 'description')
