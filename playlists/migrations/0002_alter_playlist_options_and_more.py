# Generated by Django 4.2 on 2024-02-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['-created_at'], name='playlists_p_created_e97a73_idx'),
        ),
    ]
