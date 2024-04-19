from django.db import models


class Lyric(models.Model):
    class LanguageChoices(models.TextChoices):
        RU = "RU"
        EN = "EN"

    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    song = models.ForeignKey("songs.Song", on_delete=models.CASCADE)

    def __str__(self):
        return f"lyrics for {self.song.name}"

    class Meta:
        unique_together = ("language", "song")


class LyricLineTimecode(models.Model):
    lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE)
    timecode = models.IntegerField()
    text_line = models.CharField(max_length=128)

    class Meta:
        unique_together = ("timecode", "text_line")

    def __str__(self):
        return self.text_line
