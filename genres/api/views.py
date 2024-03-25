from rest_framework import generics
from genres.models import Genre
from genres.api.serializers import GenreSerializer


class GenreListAPIView(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

