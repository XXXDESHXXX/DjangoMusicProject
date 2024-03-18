from django.urls import path, include

app_name = 'genres'

urlpatterns = [
    path("api/", include("genres.api.urls", namespace="api")),
]
