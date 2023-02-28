from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Данное действие доступно только администратору.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)
