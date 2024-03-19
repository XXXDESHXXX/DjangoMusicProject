from django.test import TestCase
from genres.models import Genre
from genres.api.serializers import GenreSerializer


class GenreSerializerTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test Genre')
        self.serializer = GenreSerializer(instance=self.genre)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), ({'id', 'name'}))

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.genre.id) 

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Genre')

    def test_create_valid_genre(self):
        serializer = GenreSerializer(data={'name': 'Test Genre'})
        self.assertTrue(serializer.is_valid())
