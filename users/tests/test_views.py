from http import HTTPStatus

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory, APIClient
from users.models import User, UserFollow
from users.api.views import UserFollowCreateAPIView


class UserFollowCreateAPIViewTestCase(TestCase):
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
