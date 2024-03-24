from django.test import TestCase
from users.models import User
from songs.models import Song, UserSongLike
from genres.models import Genre
from songs.api.serializers import SongSerializer


class SongSerializerTest(TestCase):
    def setUp(self) -> None:
        genre = Genre.objects.create(name="Rock")
        user = User.objects.create(username="test_user")
        song = Song.objects.create(
            name="Test Song", file="test_song.mp3", genre=genre, user=user
        )
        UserSongLike.objects.create(user=user, liked_song=song)

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
