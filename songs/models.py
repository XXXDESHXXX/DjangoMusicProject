from django.db import models

from genres.models import Genre
from users.models import User


class Song(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=64)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
