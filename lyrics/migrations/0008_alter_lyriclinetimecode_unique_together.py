# Generated by Django 4.2 on 2024-05-27 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lyrics", "0007_rename_timecode_new_lyriclinetimecode_timecode_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lyriclinetimecode",
            unique_together={("lyric", "timecode")},
        ),
    ]
