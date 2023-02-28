from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Позволяет редактировать контент только автору."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Позволяет редактировать контент только автору, админу, модератору."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                )