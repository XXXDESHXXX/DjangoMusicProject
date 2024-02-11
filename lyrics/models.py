from django.db import models


class Lyric(models.Model):
    class LanguageChoices(models.TextChoices):
        RU = "RU"
        EN = "EN"
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    song = models.ForeignKey("songs.Song", on_delete=models.CASCADE)


class LyricLineTimecode(models.Model):
    lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE)
    timecode = models.DurationField()
    text_line = models.CharField(max_length=128)
