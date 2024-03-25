from django.test import TestCase
from users.models import User
from playlists.models import Playlist
from playlists.api.serializers import PlaylistSerializer


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
