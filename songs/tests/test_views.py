from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from genres.models import Genre
from songs.models import Song
from users.models import User


class SongListAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        genre = Genre.objects.create(name="Test Genre")
        self.song1 = Song.objects.create(
            name="Song 1", file="song1.mp3", genre=genre, user=self.user
        )
        self.song2 = Song.objects.create(
            name="Song 2", file="song2.mp3", genre=genre, user=self.user
        )

    def test_song_list(self) -> None:
        url = reverse("songs:api:song_list")
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Song.objects.count())
        for song_data, expected_song in zip(response.data, [self.song1, self.song2]):
            self.assertEqual(song_data["id"], expected_song.id)
            self.assertEqual(song_data["name"], expected_song.name)
            self.assertEqual(
                song_data["file"], f"http://testserver{expected_song.file.url}"
            )

    def test_song_list_empty(self) -> None:
        Song.objects.all().delete()
        url = reverse("songs:api:song_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
