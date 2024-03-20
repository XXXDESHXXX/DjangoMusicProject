from django.contrib import admin
from .models import Lyric, LyricLineTimecode


@admin.register(Lyric)
class LyricAdmin(admin.ModelAdmin):
    list_display = ["language", "song"]


@admin.register(LyricLineTimecode)
class LyricLineTimecodeAdmin(admin.ModelAdmin):
    list_display = ["lyric", "timecode", "text_line"]
