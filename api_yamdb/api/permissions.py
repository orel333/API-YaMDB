import logging
import sys

from rest_framework.permissions import SAFE_METHODS, BasePermission

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s - строка %(lineno)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
handler.setFormatter(formatter)
logger.disabled = False
logger.debug('Логирование из permissions запущено')


class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        logger.debug(f'dir request: {dir(request)}')
        logger.debug('IsAdminUserCustomPermission запущен, уровень запроса.')
        logger.debug(request.user.role)
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
