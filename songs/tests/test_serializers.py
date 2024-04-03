from django.test import TestCase
from users.models import User
from songs.models import Song, UserSongLike
from genres.models import Genre
from songs.api.serializers import SongSerializer, UserSongLikeSerializer


class SongSerializerTest(TestCase):
    def setUp(self) -> None:
        genre = Genre.objects.create(name="Rock")
        user = User.objects.create(username="test_user")
        song = Song.objects.create(
            name="Test Song", file="test_song.mp3", genre=genre, user=user
        )

    def test_song_serializer(self) -> None:
        song = Song.objects.first()
        serializer = SongSerializer(song)

        self.assertEqual(serializer.data["id"], song.id)
        self.assertEqual(serializer.data["name"], song.name)
        self.assertEqual(serializer.data["file"], song.file.url)
        self.assertEqual(serializer.data["genre"], song.genre.id)
        self.assertEqual(serializer.data["user"], song.user.id)

    def test_song_serializer_fields(self) -> None:
        serializer = SongSerializer()
        expected_fields = ["id", "name", "file", "likes", "genre", "user"]
        self.assertEqual(set(serializer.fields.keys()), set(expected_fields))


class UserSongLikeSerializerTest(TestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(name="Jazz")
        self.user = User.objects.create(username="test_user")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user=self.user
        )
        self.usersonglike_data = {
            "user": self.user.id,
            "liked_song": self.song.id,
            "created_at": "2024-03-26T12:00:00Z",
        }
        self.serializer = UserSongLikeSerializer(data=self.usersonglike_data)

    def test_valid_data(self) -> None:
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data_missing_fields(self) -> None:
        invalid_data = {"created_at": "2024-03-26T12:00:00Z"}
        serializer = UserSongLikeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_user_field_content(self) -> None:
        self.assertTrue(self.serializer.is_valid())
        data = self.serializer.data
        self.assertEqual(data["user"], self.usersonglike_data["user"])

    def test_liked_song_field_content(self) -> None:
        self.assertTrue(self.serializer.is_valid())
        data = self.serializer.data
        self.assertEqual(data["liked_song"], self.usersonglike_data["liked_song"])
