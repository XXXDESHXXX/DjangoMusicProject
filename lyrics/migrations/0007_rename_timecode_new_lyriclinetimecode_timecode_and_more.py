# Generated by Django 4.2 on 2024-04-19 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lyrics", "0006_alter_lyriclinetimecode_unique_together_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lyriclinetimecode",
            old_name="timecode_new",
            new_name="timecode",
        ),
        migrations.AlterUniqueTogether(
            name="lyriclinetimecode",
            unique_together={("timecode", "text_line")},
        ),
    ]