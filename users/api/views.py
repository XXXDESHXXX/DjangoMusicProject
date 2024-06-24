from typing import Any

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from users.models import UserFollow
from .serializers import UserFollowCreateSerializer

User = get_user_model()


class UserFollowCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowCreateSerializer

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    "error": "IntegrityError",
                    "detail": "You cannot follow the same user twice.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context["user_from"] = self.request.user
        return context

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user_from=self.request.user)


class UserFollowDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserFollow:
        user_id = self.kwargs.get("user_id")
        user_to = get_object_or_404(User, id=user_id)
        user_from = self.request.user
        return get_object_or_404(UserFollow, user_from=user_from, user_to=user_to)
