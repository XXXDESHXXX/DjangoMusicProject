from rest_framework import generics
from genres.models import Genre
from genres.api.serializers import GenreSerializer


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
