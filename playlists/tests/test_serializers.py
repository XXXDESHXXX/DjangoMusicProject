from datetime import datetime, timezone

from django.utils import timezone
from django.test import TestCase

from genres.models import Genre
from songs.models import Song
from users.models import User
from playlists.models import Playlist, PlaylistSong
from playlists.api.serializers import PlaylistSerializer, PlaylistSongSerializer


class PlaylistSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user")
        self.playlist_data = {
            "name": "Test Playlist",
            "image": "/test.jpg",
            "is_private": False,
            "description": "This is a test playlist.",
        }
        self.playlist = Playlist.objects.create(user=self.user, **self.playlist_data)
        self.serializer = PlaylistSerializer(instance=self.playlist)

    def test_contains_expected_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {
                "name",
                "image",
                "created_at",
                "updated_at",
                "is_private",
                "description",
            },
        )

    def test_name_field_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["name"], self.playlist_data["name"])

    def test_image_field_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["image"], self.playlist_data["image"])

    def test_is_private_field_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["is_private"], self.playlist_data["is_private"])

    def test_description_field_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["description"], self.playlist_data["description"])


class PlaylistSongSerializerTest(TestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(name="Rock")
        self.user = User.objects.create(username="test_user")
        self.playlist = Playlist.objects.create(user=self.user, name="Test Playlist")
        self.song = Song.objects.create(
            name="Example Song", genre_id=self.genre.id, user=self.user
        )
        self.playlist_song_data = {
            "id": self.song.id,
            "created_at": "2024-03-26T12:00:00Z",
            "song": self.song.id,
        }
        self.serializer = PlaylistSongSerializer(data=self.playlist_song_data)

    def test_valid_data(self) -> None:
        self.assertTrue(self.serializer.is_valid())

    def test_id_field_content(self) -> None:
        self.assertTrue(self.serializer.is_valid())
        data = self.serializer.data
        self.assertEqual(data["song"], self.playlist_song_data["song"])

    def test_invalid_data_missing_fields(self) -> None:
        invalid_data = {"created_at": "2024-03-26T12:00:00Z"}
        serializer = PlaylistSongSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
