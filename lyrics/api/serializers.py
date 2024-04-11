from rest_framework import serializers
from lyrics.models import Lyric, LyricLineTimecode


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ("language", "song_id")


class LyricLineTimecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LyricLineTimecode
        fields = ("timecode", "text_line")
