<<<<<<< HEAD
from rest_framework import permissions

from .views import logger


class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.debug('IsAdminUserCustomPermission запущен, уровень запроса.')
        logger.debug(self.request.user.role)
        return request.user.is_authenticated
=======
from rest_framework import permissions

from .views import logger


class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.debug('IsAdminUserCustomPermission запущен, уровень запроса.')
        logger.debug(self.request.user.role)
        return request.user.is_authenticated
>>>>>>> master
