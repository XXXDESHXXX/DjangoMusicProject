from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from genres.models import Genre
from songs.models import Song, UserSongLike
from users.models import User


class UserSongLikeCreateAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user")
        self.genre = Genre.objects.create(name="Jazz")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("songs:api:user_like_create")

    def test_create_usersonglike(self) -> None:
        data = {"liked_song": self.song.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_usersonglike(self) -> None:
        UserSongLike.objects.create(user=self.user, liked_song=self.song)

        data = {"liked_song": self.song.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserSongLikeDeleteAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test_user")
        self.genre = Genre.objects.create(name="Jazz")
        self.song = Song.objects.create(
            name="Test Song", genre_id=self.genre.id, user=self.user
        )
        self.usersonglike = UserSongLike.objects.create(
            user=self.user, liked_song=self.song
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse(
            "songs:api:user_like_delete", kwargs={"song_id": self.song.id}
        )

    def test_delete_usersonglike(self) -> None:
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserSongLike.objects.filter(id=self.usersonglike.id).exists())

    def test_delete_nonexistent_usersonglike(self) -> None:
        non_existent_song_id = self.song.id + 1
        url = reverse(
            "songs:api:user_like_delete", kwargs={"song_id": non_existent_song_id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
