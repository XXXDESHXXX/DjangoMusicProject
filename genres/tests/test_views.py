from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from genres.models import Genre
from genres.api.serializers import GenreSerializer


class GenreListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("genres:api:genre_list")
        self.genre1 = Genre.objects.create(name="Genre 1")
        self.genre2 = Genre.objects.create(name="Genre 2")

    def test_get_genre_list(self):
        response = self.client.get(self.url)
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
