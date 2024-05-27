from urllib.request import Request

from django.core.exceptions import PermissionDenied
from django.db.models import Model
from django.views import View
from rest_framework import permissions

from songs.models import Song
from users.models import User


class IsMusician(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.role == User.RoleChoices.MUSICIAN


class IsCurrentUserEqualsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return obj.user == request.user  # noqa
