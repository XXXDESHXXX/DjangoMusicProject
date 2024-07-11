import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from songs.constants import VALID_EXTENSIONS, VALID_MIME_TYPES


def validate_song_file(value: UploadedFile) -> None:
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError("Unsupported file extension.")

    if value.content_type not in VALID_MIME_TYPES:
        raise ValidationError("Unsupported file type.")
