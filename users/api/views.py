from typing import Any

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from users.models import UserFollow
from .serializers import UserFollowCreateSerializer, UserFollowSerializer

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


class UserFollowListAPIView(ListAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return UserFollow.objects.filter(user_from=user_id)


class UserFollowDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowSerializer

    def get_object(self) -> UserFollow:
        return get_object_or_404(UserFollow, id=self.kwargs.get("user_follow_id"))

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        follow = self.get_object()

        if follow.user_from != request.user:
            return Response(
                {
                    "Error": "Bad Request",
                    "detail": "You don't have permission for this action.",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(follow)
        return Response(status=status.HTTP_204_NO_CONTENT)
