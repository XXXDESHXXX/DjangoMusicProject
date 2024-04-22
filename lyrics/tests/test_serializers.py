from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from genres.models import Genre
from lyrics.models import Lyric, LyricLineTimecode
from lyrics.api.serializers import LyricSerializer, LyricLineTimecodeSerializer, LyricLineTimecodeValidSerializer
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


class LyricLineTimecodeSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test1 user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.timecode = 1
        self.text_line = "Some text line"
        self.lyric_line_timecode = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode=self.timecode, text_line=self.text_line
        )

    def test_serializer_data(self) -> None:
        serializer = LyricLineTimecodeSerializer(instance=self.lyric_line_timecode)
        expected_data = {
            "timecode": 1,
            "text_line": self.lyric_line_timecode.text_line,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self) -> None:
        invalid_data = {"timecode": "invalid_timecode_format", "text_line": ""}
        serializer_with_invalid_data = LyricLineTimecodeSerializer(data=invalid_data)
        self.assertFalse(serializer_with_invalid_data.is_valid())

        valid_data = {
            "timecode": 12,
            "text_line": "New text line",
        }
        serializer_with_valid_data = LyricLineTimecodeSerializer(data=valid_data)
        self.assertTrue(serializer_with_valid_data.is_valid())


class LyricLineTimecodeValidSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test12 user")
        self.genre = Genre.objects.create(name="Test1 Genre")
        self.song = Song.objects.create(
            name="Test1 Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.timecode = 1
        self.text_line = "Some text line"
        self.lyric_line_timecode = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode=self.timecode, text_line=self.text_line
        )

    def test_create_negative_timecode(self) -> None:
        invalid_data = {"timecode": -1, "text_line": "123456"}

        serializer_with_invalid_data = LyricLineTimecodeValidSerializer(data=invalid_data)
        self.assertFalse(serializer_with_invalid_data.is_valid())

        valid_data = {
            "timecode": 12,
            "text_line": "New text line",
        }

        serializer_with_valid_data = LyricLineTimecodeValidSerializer(data=valid_data)
        self.assertTrue(serializer_with_valid_data.is_valid())
