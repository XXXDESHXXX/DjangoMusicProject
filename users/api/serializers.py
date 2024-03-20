from rest_framework import serializers
from users.models import UserFollow


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ("id", "user_from", "user_to", "created")
        read_only_fields = ("created",)


class UserFollowCreateSerializer(UserFollowSerializer):

    class Meta(UserFollowSerializer.Meta):
        read_only_fields = UserFollowSerializer.Meta.read_only_fields + ("user_from",)
