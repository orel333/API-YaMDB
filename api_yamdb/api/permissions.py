from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminModeratorUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
            or request.user.is_authenticated
        )
        
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.admin
        )
        



class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.role == 'admin'


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
