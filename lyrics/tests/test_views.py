from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from genres.models import Genre
from lyrics.models import Lyric, LyricLineTimecode
from songs.models import Song
from lyrics.api.serializers import LyricSerializer, LyricLineTimecodeSerializer
from users.models import User


class LyricSongAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric1 = Lyric.objects.create(language="EN", song=self.song)
        self.lyric2 = Lyric.objects.create(language="RU", song=self.song)

    def test_get_lyrics_for_song(self) -> None:
        url = reverse("lyrics:api:lyric_song_list", kwargs={"song_id": self.song.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = LyricSerializer([self.lyric1, self.lyric2], many=True).data
        self.assertEqual(response.data, expected_data)


class LyricDeleteAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song_id=self.song.id)

    def test_delete_lyric(self) -> None:
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": self.lyric.id})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lyric.objects.filter(id=self.lyric.id).exists())

    def test_delete_nonexistent_lyric(self) -> None:
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": 999})
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LyricCreateAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(name="Metal")
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.valid_payload = {"language": "RU", "song_id": self.song.id}
        self.existing_lyric = Lyric.objects.create(language="EN", song_id=self.song.id)
        self.invalid_payload = {"language": "EN", "song_id": self.song.id}

    def test_create_lyric_valid_song_id(self) -> None:
        url = reverse("lyrics:api:create_lyric", kwargs={"song_id": self.song.id})
        response = self.client.post(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lyric_duplicate_language(self) -> None:
        url = reverse("lyrics:api:create_lyric", kwargs={"song_id": self.song.id})
        response = self.client.post(url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "You cannot add the same language twice"
        )


class LyricLineTimecodeListAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line1 = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode="00:03:03", text_line="asdhfas"
        )
        self.lyric_line2 = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode="00:04:05", text_line="asdhfasss"
        )

    def test_get_lyrics_for_song(self) -> None:
        url = reverse(
            "lyrics:api:lyric_line_timecode_list", kwargs={"lyric_id": self.lyric.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LyricLineTimecodeDeleteAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test user1")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode="00:03:03", text_line="asdf"
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_lyric_line_timecode(self) -> None:
        url = reverse(
            "lyrics:api:delete_lyric_line_timecode",
            kwargs={"lyric_line_timecode_id": self.lyric_line.id},
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            LyricLineTimecode.objects.filter(id=self.lyric_line.id).exists()
        )

    def test_delete_playlist_unauthenticated(self) -> None:
        self.client.logout()
        url = reverse(
            "lyrics:api:delete_lyric_line_timecode",
            kwargs={"lyric_line_timecode_id": self.lyric_line.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LyricLineTimecodeCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test USERNAME")
        self.genre = Genre.objects.create(name="Test GENRE")
        self.song = Song.objects.create(
            name="Test SONG", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode="00:03:03", text_line="asdf"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lyric_line_timecode(self) -> None:
        data = {
            "lyric_id": self.lyric.id,
            "timecode": "03:03:03",
            "text_line": "text_line123456",
        }

        response = self.client.post(
            reverse(
                "lyrics:api:create_lyric_line_timecode",
                kwargs={"lyric_id": self.lyric.id},
            ),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            LyricLineTimecode.objects.filter(
                lyric_id=self.lyric.id, timecode="03:03:03", text_line="text_line123456"
            ).exists()
        )


