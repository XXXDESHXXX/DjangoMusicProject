from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import UserFollow
from .serializers import UserFollowCreateSerializer

User = get_user_model()


class UserFollowCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowCreateSerializer

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user_from=self.request.user)


class UserFollowDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserFollow:
        user_id = self.kwargs.get("user_id")
        user_to = get_object_or_404(User, id=user_id)
        user_from = self.request.user
        return get_object_or_404(UserFollow, user_from=user_from, user_to=user_to)
