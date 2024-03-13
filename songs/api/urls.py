from django.urls import path

from songs.api.views import UserSongLikeCreateAPIView

app_name = 'songs'

urlpatterns = [
    path('songs/likes/create/', UserSongLikeCreateAPIView.as_view(), name='user_like_create'),
]
