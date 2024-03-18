from django.urls import path

from genres.api.views import GenreListView

app_name = 'genres'

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre_list'),
]
