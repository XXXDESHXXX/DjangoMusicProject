from rest_framework import permissions

from users.models import User


class IsMusician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.RoleChoices.MUSICIAN
