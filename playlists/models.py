from django.db import models

from songs.models import Song
from users.models import User


class PlaylistSong(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song,
                             on_delete=models.CASCADE
                             )


class Playlist(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    description = models.CharField(blank=True, null=True, max_length=255)
    user = models.ForeignKey(User,
                             related_name='playlists',
                             on_delete=models.PROTECT
                             )
    songs = models.ManyToManyField(PlaylistSong)
