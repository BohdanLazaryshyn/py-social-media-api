from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user.profile


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.subscriber == request.user.profile or request.user.is_staff


class IsAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
