from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from users.api.serializers import UserFollowSerializer, UserFollowCreateSerializer
from users.models import User, UserFollow


class UserFollowSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="user1",
            description="Description of user 1",
        )
        self.user2 = User.objects.create(
            username="user2",
            description="Description of user 2",
        )
        self.user_follow_data = {
            "user_from": self.user1.pk,
            "user_to": self.user2.pk,
        }

    def test_user_follow_serializer(self):
        serializer = UserFollowSerializer(data=self.user_follow_data)
        self.assertTrue(serializer.is_valid())
        user_follow_object = serializer.save()

        self.assertEqual(user_follow_object.user_from, self.user1)
        self.assertEqual(user_follow_object.user_to, self.user2)
