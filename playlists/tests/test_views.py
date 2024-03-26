from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
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
