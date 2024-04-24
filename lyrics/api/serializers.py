from rest_framework import serializers
from lyrics.models import Lyric, LyricLineTimecode


class LyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = ("id", "language", "song_id")


class LyricLineTimecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LyricLineTimecode
        fields = ("id", "timecode", "text_line")

    def validate_timecode(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Timecode must be a non-negative integer."
            )
        return value
