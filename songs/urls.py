from django.urls import path, include

app_name = 'songs'

urlpatterns = [
    path("api/", include("songs.api.urls", namespace="api")),
]
