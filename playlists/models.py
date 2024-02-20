from django.db import models

from songs.models import Song
from users.models import User


class PlaylistSong(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song,
                             on_delete=models.CASCADE
                             )

    def __str__(self):
        return f'Playlist of {self.song.name}'


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

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f'Playlist {self.name} by {self.user}'

