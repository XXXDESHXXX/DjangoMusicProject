# Generated by Django 4.2 on 2024-04-19 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lyrics", "0005_lyriclinetimecode_timecode_new"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lyriclinetimecode",
            unique_together={("timecode_new", "text_line")},
        ),
        migrations.RemoveField(
            model_name="lyriclinetimecode",
            name="timecode",
        ),
    ]
