from django.urls import path

from genres.api.views import GenreListAPIView

app_name = "genres"

urlpatterns = [
    path("genres/", GenreListAPIView.as_view(), name="genre_list"),
]
