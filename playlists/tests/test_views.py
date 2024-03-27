from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from playlists.models import Playlist
from users.models import User


class PlaylistListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.playlist1 = Playlist.objects.create(
            name="Playlist 1", description="Description 1", user_id=self.user.id
        )
        self.playlist2 = Playlist.objects.create(
            name="Playlist 2", description="Description 2", user_id=self.user.id
        )

    def test_get_playlists(self):
        url = reverse("playlists:api:list_of_playlists")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        playlist_names = [playlist["name"] for playlist in response.data]

        self.assertIn("Playlist 1", playlist_names)
        self.assertIn("Playlist 2", playlist_names)


class UserPlaylistListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.client = APIClient()
        self.playlist1 = Playlist.objects.create(
            name="Playlist 1", description="Description 1", user_id=self.user.id
        )
        self.playlist2 = Playlist.objects.create(
            name="Playlist 2", description="Description 2", user_id=self.user.id
        )

    def test_user_playlist_list(self):
        url = reverse("playlists:api:user_playlist_list", kwargs={"user_id": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Playlist.objects.filter(user=self.user).count())

        for playlist in response.data:
            self.assertEqual(playlist["user"], self.user.id)

        expected_playlist_names = ("Playlist 2", "Playlist 1")
        returned_playlist_names = [playlist["name"] for playlist in response.data]

        self.assertEqual(expected_playlist_names, tuple(returned_playlist_names))


class PlaylistCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_playlist(self):
        data = {'name': 'Test Playlist', "user": self.user.id}

        response = self.client.post(reverse("playlists:playlists:playlist_create"), data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Playlist.objects.filter(name='Test Playlist', user=self.user).exists())

    def test_create_playlist_unauthenticated(self):
        self.client.logout()
        data = {'name': 'Test Playlist'}

        response = self.client.post(reverse("playlists:playlists:playlist_create"), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlaylistDeleteAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.playlist = Playlist.objects.create(user=self.user, name='Test Playlist')
        self.client.force_authenticate(user=self.user)

    def test_delete_playlist(self):
        url = reverse("playlists:api:playlist_delete", kwargs={'playlist_id': self.playlist.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Playlist.objects.filter(id=self.playlist.id).exists())

    def test_delete_playlist_unauthenticated(self):
        self.client.logout()
        url = reverse("playlists:api:playlist_delete", kwargs={'playlist_id': self.playlist.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_playlist_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.client.force_authenticate(user=other_user)
        url = reverse("playlists:api:playlist_delete", kwargs={'playlist_id': self.playlist.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PlaylistUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.playlist = Playlist.objects.create(user=self.user, name='Test Playlist')
        self.client.force_authenticate(user=self.user)

    def test_update_playlist(self):
        url = reverse("playlists:api:playlist_update", kwargs={'playlist_id': self.playlist.id})
        new_name = "Updated Playlist Name"
        data = {'name': new_name, "user": self.user.id}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, new_name)

    def _test_update_playlist_with_user(self, user):
        url = reverse("playlists:api:playlist_update", kwargs={'playlist_id': self.playlist.id})
        new_name = "Updated Playlist Name"
        data = {'name': new_name, "user": self.user.id}

        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        return response

    def test_update_playlist_unauthenticated(self):
        response = self._test_update_playlist_with_user(None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_playlist_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        response = self._test_update_playlist_with_user(other_user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
