# Generated by Django 4.2 on 2024-04-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lyrics", "0004_alter_lyriclinetimecode_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="lyriclinetimecode",
            name="timecode_new",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
