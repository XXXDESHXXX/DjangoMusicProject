from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from genres.models import Genre
from lyrics.models import Lyric
from songs.models import Song
from lyrics.api.serializers import LyricSerializer
from users.models import User


class LyricSongAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric1 = Lyric.objects.create(language="EN", song=self.song)
        self.lyric2 = Lyric.objects.create(language="RU", song=self.song)

    def test_get_lyrics_for_song(self):
        url = reverse("lyrics:api:lyric_song_list", kwargs={"song_id": self.song.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = LyricSerializer([self.lyric1, self.lyric2], many=True).data
        self.assertEqual(response.data, expected_data)


class LyricDeleteAPIViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song_id=self.song.id)

    def test_delete_lyric(self):
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": self.lyric.id})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lyric.objects.filter(id=self.lyric.id).exists())

    def test_delete_nonexistent_lyric(self):
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": 999})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
