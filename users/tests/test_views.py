from http import HTTPStatus

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from users.models import User, UserFollow
from users.api.views import UserFollowCreateAPIView


class UserFollowCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="test_user2", password="testpassword"
        )

    def test_user_follow_create_api_view_authenticated_user(self):
        request = self.factory.post(
            "/api/user_follow_create/", data={"user_to": self.user2.id}
        )
        request.user = self.user

        response = UserFollowCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        self.assertTrue(
            UserFollow.objects.filter(user_from=self.user, user_to=self.user2).exists()
        )

    def test_user_follow_create_api_view_anonymous_user(self):
        request = self.factory.post("/api/user-follow-create/")
        request.user = AnonymousUser()

        response = UserFollowCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        self.assertFalse(
            UserFollow.objects.filter(user_from=self.user, user_to=self.user2).exists()
        )


class UserFollowDeleteAPIViewTest(APITestCase):
    def setUp(self):
        self.user_from = User.objects.create(username="user_from")
        self.user_to = User.objects.create(username="user_to")
        self.user_follow = UserFollow.objects.create(
            user_from=self.user_from, user_to=self.user_to
        )
        self.client.force_authenticate(user=self.user_from)
        self.url = reverse(
            "users:api:user_follow_delete", kwargs={"user_id": self.user_to.id}
        )

    def test_delete_user_follow(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserFollow.objects.filter(id=self.user_follow.id).exists())

    def test_delete_nonexistent_user_follow(self):
        non_existent_user_id = self.user_to.id + 1
        url = reverse(
            "users:api:user_follow_delete", kwargs={"user_id": non_existent_user_id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
