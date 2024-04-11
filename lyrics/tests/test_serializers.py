from django.test import TestCase

from genres.models import Genre
from lyrics.models import Lyric
from lyrics.api.serializers import LyricSerializer
from songs.models import Song
from users.models import User


class LyricSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test User")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric_data = {
            "language": "EN",
            "song_id": self.song.id,
        }
        self.lyric = Lyric.objects.create(**self.lyric_data)
        self.serializer = LyricSerializer(instance=self.lyric)

    def test_serializer_contains_expected_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"language", "song_id"})

    def test_serializer_fields_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["language"], self.lyric_data["language"])
        self.assertEqual(data["song_id"], self.lyric_data["song_id"])

    def test_serializer_validation(self) -> None:
        serializer_with_empty_data = LyricSerializer(data={})
        self.assertFalse(serializer_with_empty_data.is_valid())

        serializer_with_valid_data = LyricSerializer(data=self.lyric_data)
        self.assertTrue(serializer_with_valid_data.is_valid())
