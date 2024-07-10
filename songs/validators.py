import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


def validate_song_file(value: UploadedFile) -> None:
    valid_mime_types = ("audio/mpeg", "audio/mp3", "audio/wav")
    valid_extensions = (".mp3", ".wav")
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension.")

    if value.content_type not in valid_mime_types:
        raise ValidationError("Unsupported file type.")
