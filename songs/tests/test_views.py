from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from genres.models import Genre
from songs.models import Song, UserSongLike
from users.models import User
from utils.permissions import IsMusician


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


class SongCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Jazz")
        self.user = User.objects.create_user(username='testuser', password='password')
        self.musician_user = User.objects.create_user(username='musicianuser', password='password',
                                                      role=User.RoleChoices.MUSICIAN)
        self.url = reverse('songs:api:create_song')

    def test_create_song_unauthenticated(self):
        data = {
            'name': 'New Song',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_song_without_musician_permission(self):
        self.client.login(username='testuser', password='password')
        data = {
            'name': 'New Song',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_song_with_missing_fields(self):
        self.client.login(username='musicianuser', password='password')
        data = {
            'name': '',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SongDeleteAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Jazz")
        self.user = User.objects.create_user(username='testuser', password='password')
        self.musician_user = User.objects.create_user(username='musicianuser', password='password',
                                                      role=User.RoleChoices.MUSICIAN)
        self.song = Song.objects.create(name='Test Song', genre=self.genre, user=self.musician_user)
        self.url = reverse('songs:api:delete_song', kwargs={'song_id': self.song.id})

    def test_delete_song_successfully(self):
        self.client.login(username='musicianuser', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Song.objects.filter(id=self.song.id).exists())

    def test_delete_song_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_song_without_musician_permission(self):
        self.client.login(username='testuser', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_song_not_owner(self):
        another_musician = User.objects.create_user(username='anothermusician', password='password', role=User.RoleChoices.MUSICIAN)
        self.client.login(username='anothermusician', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_existent_song(self):
        self.client.login(username='musicianuser', password='password')
        non_existent_url = reverse('songs:api:delete_song', kwargs={'song_id': 9999})
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)