from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.owner == request.user:
            return True
        return False

        # Instance must have an attribute named `owner`.
        # return obj.owner == request.user
