# Generated by Django 4.2 on 2024-04-18 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lyrics", "0003_alter_lyric_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lyriclinetimecode",
            unique_together={("timecode", "text_line")},
        ),
    ]