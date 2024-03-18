from rest_framework import generics
from genres.models import Genre
from genres.api.serializers import GenreSerializer


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
