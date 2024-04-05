from django.urls import path, include

app_name = "lyrics"

urlpatterns = [
    path("api/", include("lyrics.api.urls", namespace="api")),
]
