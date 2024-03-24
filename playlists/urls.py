from django.urls import path, include

app_name = "playlists"

urlpatterns = [
    path("api/", include("playlists.api.urls", namespace="api")),
]
