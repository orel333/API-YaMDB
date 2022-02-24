import logging
import sys

from rest_framework import permissions

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


class IsAdminUserCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        logger.debug(f'dir request: {dir(request)}')
        logger.debug('IsAdminUserCustomPermission запущен, уровень запроса.')
        logger.debug(request.user.role)
        return request.user.is_staff is True
