from django.contrib.auth.models import AbstractUser
from django.db import models


class UserFollow(models.Model):
    user_from = models.ForeignKey(
        "users.User",
        related_name="rel_from_set",
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        "users.User",
        related_name="rel_to_set",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "user", "User"
        MUSICIAN = "musician", "Musician"

    description = models.CharField(max_length=255)
    role = models.CharField(max_length=16, choices=RoleChoices.choices, default=RoleChoices.USER.value)
    image = models.ImageField(blank=True, null=True, upload_to="users")
    is_private = models.BooleanField(default=False)
    following = models.ManyToManyField('self',
                                       through=UserFollow,
                                       )
    listens = models.ManyToManyField("songs.Song", related_name="user_who_listen")
