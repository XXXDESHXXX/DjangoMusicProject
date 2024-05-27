from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
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
        self.user = User.objects.create(
            username="Test user", role=User.RoleChoices.MUSICIAN
        )
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song_id=self.song.id)
        self.client.force_login(self.user)

    def test_delete_lyric(self) -> None:
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": self.lyric.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lyric.objects.filter(id=self.lyric.id).exists())

    def test_delete_nonexistent_lyric(self) -> None:
        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_lyric_by_another_user(self) -> None:
        other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )
        self.client.force_login(user=other_user)

        url = reverse("lyrics:api:delete_lyric", kwargs={"lyric_id": self.lyric.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lyric.objects.filter(pk=self.lyric.id).exists())


class LyricCreateAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.genre = Genre.objects.create(name="Metal")
        self.musician_user = User.objects.create(
            username="musician", password="testpassword", role=User.RoleChoices.MUSICIAN
        )
        self.client.force_authenticate(user=self.musician_user)
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.musician_user.id
        )
        self.valid_payload = {"language": "RU", "song_id": self.song.id}
        self.existing_lyric = Lyric.objects.create(language="EN", song_id=self.song.id)

        self.other_user = User.objects.create(
            username="otheruser", password="testpassword"
        )

    def test_create_lyric_with_valid_data(self) -> None:
        url = reverse("lyrics:api:create_lyric", kwargs={"song_id": self.song.id})
        response = self.client.post(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lyric_with_other_user(self) -> None:
        self.client.force_authenticate(user=self.other_user)

        url = reverse("lyrics:api:create_lyric", kwargs={"song_id": self.song.id})
        response = self.client.post(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LyricLineTimecodeListAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Test user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line1 = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode=12, text_line="asdhfas"
        )
        self.lyric_line2 = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode=123, text_line="asdhfasss"
        )

    def test_get_lyrics_for_song(self) -> None:
        url = reverse(
            "lyrics:api:lyric_line_timecode_list", kwargs={"lyric_id": self.lyric.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LyricLineTimecodeDeleteAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username="Test user1", role=User.RoleChoices.MUSICIAN
        )
        self.other_user = User.objects.create(username="Other user")
        self.genre = Genre.objects.create(name="Test Genre")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line = LyricLineTimecode.objects.create(
            lyric=self.lyric, timecode=13, text_line="asdf"
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

    def test_delete_unauthenticated(self) -> None:
        self.client.logout()
        url = reverse(
            "lyrics:api:delete_lyric_line_timecode",
            kwargs={"lyric_line_timecode_id": self.lyric_line.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_by_another_user(self) -> None:
        other_user = User.objects.create_user(
            username="otheruser1", password="testpassword"
        )
        self.client.force_authenticate(user=other_user)

        url = reverse(
            "lyrics:api:delete_lyric_line_timecode",
            kwargs={"lyric_line_timecode_id": self.lyric_line.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            LyricLineTimecode.objects.filter(pk=self.lyric_line.id).exists()
        )


class LyricLineTimecodeCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username="Test USERNAME", role=User.RoleChoices.MUSICIAN
        )
        self.genre = Genre.objects.create(name="Test GENRE")
        self.song = Song.objects.create(
            name="Test SONG", genre_id=self.genre.id, user_id=self.user.id
        )
        self.lyric = Lyric.objects.create(language="RU", song=self.song)
        self.lyric_line = LyricLineTimecode.objects.create(
            lyric_id=self.lyric.id, timecode=1, text_line="asdf"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_by_another_user(self) -> None:
        other_user = User.objects.create(username="Other user")
        self.client.force_authenticate(user=other_user)

        data = {
            "lyric_id": self.lyric.id,
            "timecode": 2,
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(
            LyricLineTimecode.objects.filter(
                lyric_id=self.lyric.id, timecode=2, text_line="text_line123456"
            ).exists()
        )
