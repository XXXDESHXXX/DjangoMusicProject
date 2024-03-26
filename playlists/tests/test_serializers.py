from datetime import datetime, timezone

from django.utils import timezone
from django.test import TestCase

from genres.models import Genre
from songs.models import Song
from users.models import User
from playlists.models import Playlist, PlaylistSong
from playlists.api.serializers import PlaylistSerializer, PlaylistSongSerializer


class PlaylistSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.playlist_data = {
            "name": "Test Playlist",
            "image": "/test.jpg",
            "is_private": False,
            "description": "This is a test playlist.",
        }
        self.playlist = Playlist.objects.create(user=self.user, **self.playlist_data)
        self.serializer = PlaylistSerializer(instance=self.playlist)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "name",
                "image",
                "created_at",
                "updated_at",
                "is_private",
                "description",
            },
        )

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.playlist_data["name"])

    def test_image_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["image"], self.playlist_data["image"])

    def test_is_private_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["is_private"], self.playlist_data["is_private"])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["description"], self.playlist_data["description"])


class PlaylistSongSerializerTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Rock")
        self.user = User.objects.create(username="test_user")
        self.playlist = Playlist.objects.create(user=self.user, name="Test Playlist")
        self.song = Song.objects.create(
            name="Example Song", genre_id=self.genre.id, user=self.user
        )
        self.playlist_song_data = {
            "id": 1,
            "created_at": "2024-03-26T12:00:00Z",
            "song": self.song.id,
        }
        self.serializer = PlaylistSongSerializer(data=self.playlist_song_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data_missing_fields(self):
        invalid_data = {"created_at": "2024-03-26T12:00:00Z"}
        serializer = PlaylistSongSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
