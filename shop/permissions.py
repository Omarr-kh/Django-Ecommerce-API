from rest_framework import permissions


class IsAuthenticatedOrAdmin(permissions.BasePermission):
    """
    Allows access only to authenticated users or admins.
    """

    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_authenticated)
            or (request.user and request.user.is_staff)
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
