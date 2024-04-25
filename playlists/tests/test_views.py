from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient

from genres.models import Genre
from playlists.models import Playlist, PlaylistSong
from songs.models import Song
from users.models import User


class UserPlaylistListAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user")
        self.client = APIClient()
        self.playlist1 = Playlist.objects.create(
            name="Playlist 1", description="Description 1", user_id=self.user.id
        )
        self.playlist2 = Playlist.objects.create(
            name="Playlist 2", description="Description 2", user_id=self.user.id
        )

    def test_user_playlist_list(self) -> None:
        url = reverse(
            "playlists:api:user_playlist_list", kwargs={"user_id": self.user.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), Playlist.objects.filter(user=self.user).count()
        )


class PlaylistCreateAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_playlist(self) -> None:
        data = {"name": "Test Playlist", "user": self.user.id}

        response = self.client.post(
            reverse("playlists:api:playlist_create"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Playlist.objects.filter(name="Test Playlist", user=self.user).exists()
        )

    def test_create_playlist_unauthenticated(self) -> None:
        self.client.logout()
        data = {"name": "Test Playlist"}

        response = self.client.post(
            reverse("playlists:api:playlist_create"), data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlaylistDeleteAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.playlist = Playlist.objects.create(user=self.user, name="Test Playlist")
        self.client.force_authenticate(user=self.user)

    def test_delete_playlist(self) -> None:
        url = reverse(
            "playlists:api:playlist_delete", kwargs={"playlist_id": self.playlist.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Playlist.objects.filter(id=self.playlist.id).exists())

    def test_delete_playlist_unauthenticated(self) -> None:
        self.client.logout()
        url = reverse(
            "playlists:api:playlist_delete", kwargs={"playlist_id": self.playlist.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_playlist_wrong_user(self) -> None:
        other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )
        self.client.force_authenticate(user=other_user)
        url = reverse(
            "playlists:api:playlist_delete", kwargs={"playlist_id": self.playlist.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlaylistUpdateAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.playlist = Playlist.objects.create(user=self.user, name="Test Playlist")
        self.client.force_authenticate(user=self.user)

    def test_update_playlist(self) -> None:
        url = reverse(
            "playlists:api:playlist_update", kwargs={"playlist_id": self.playlist.id}
        )
        new_name = "Updated Playlist Name"
        data = {"name": new_name, "user": self.user.id}

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, new_name)

    def _test_update_playlist_with_user(self, user: User) -> Response:
        url = reverse(
            "playlists:api:playlist_update", kwargs={"playlist_id": self.playlist.id}
        )
        new_name = "Updated Playlist Name"
        data = {"name": new_name, "user": self.user.id}

        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format="json")

        return response

    def test_update_playlist_unauthenticated(self) -> None:
        response = self._test_update_playlist_with_user(None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_playlist_wrong_user(self) -> None:
        other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )
        response = self._test_update_playlist_with_user(other_user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlaylistSongCreateAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.genre = Genre.objects.create(name="Rock123")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )

        self.client.force_authenticate(user=self.user)
        self.playlist = Playlist.objects.create(name="Test Playlist", user=self.user)

        self.valid_payload = {"song": self.song.id, "playlist_id": self.playlist.id}
        self.invalid_payload = {"song": self.song.id, "playlist_id": 999}

        self.playlist_song = PlaylistSong.objects.create(
            song=self.song, playlist=self.playlist
        )

    def test_create_playlist_song_success(self) -> None:
        url = reverse(
            "playlists:api:create_playlist_song",
            kwargs={"playlist_id": self.playlist.id},
        )
        response = self.client.post(url, data=self.valid_payload, format="json")

        self.assertEqual(PlaylistSong.objects.first().song.name, "Test Song")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_playlist_song_unauthenticated(self) -> None:
        self.client.logout()
        url = reverse(
            "playlists:api:create_playlist_song",
            kwargs={"playlist_id": self.playlist.id},
        )
        response = self.client.post(url, data=self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_playlist_song_invalid_playlist_id(self) -> None:
        url = reverse("playlists:api:create_playlist_song", kwargs={"playlist_id": 999})
        response = self.client.post(url, data=self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlaylistSongDeleteAPIViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.playlist = Playlist.objects.create(name="Test Playlist", user=self.user)
        self.genre = Genre.objects.create(name="Rock Test")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user_id=self.user.id
        )

        self.playlist_song = PlaylistSong.objects.create(
            song=self.song, playlist=self.playlist
        )

    def test_delete_playlist_song_success(self) -> None:
        url = reverse(
            "playlists:api:delete_playlist_song",
            kwargs={"playlist_id": self.playlist.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PlaylistSong.objects.filter(pk=self.playlist_song.id).exists())

    def test_delete_playlist_song_unauthenticated(self) -> None:
        self.client.logout()
        url = reverse(
            "playlists:api:delete_playlist_song",
            kwargs={"playlist_id": self.playlist.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_playlist_song_not_found(self) -> None:
        url = reverse("playlists:api:delete_playlist_song", kwargs={"playlist_id": 999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
