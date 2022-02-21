import jwt
import logging
import sys

from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from users.models import CustomUser
from api.serializers import CustomUserSerializer, SignUpSerializer

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s - строка %(lineno)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
handler.setFormatter(formatter)
logger.disabled = False
logger.debug('Логирование из views запущено')

# придумать как в зависимости от эндпойнта определить список допустимых HTTP-методов
# по идее через action (methods, url_path), как user поместить в url_path

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    trailing_slash = '/'

    def get_permissions(self):
        if 'getme' in self.action_map.values():
            logger.debug('Запущен эндпойнт me')
            return (permissions.IsAuthenticated,)
        if self.suffix == 'users-list' or 'user-detail':
            logger.debug('Запущен эндпойнт users-list или user-detail')
            return (IsAdminUserCustom(),)

    @action(detail=True, url_path='me', methods=['get', 'patch'])
    def getme(self, request):
        user = get_object_or_404(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class APISignupView(APIView):

    def post(self, request):
        #email = ''
        #username = ''
        logger.debug(request.data)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
        # принимает e-mail, username,
        # формирует код подтверждения,
        # отправляет код подтверждения на e-mail
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenView(TokenViewBase):
        # принимает username, код подтверждения
        # проверяет, что информация верная, 
        # создаёт пользователя, выдает токен
    def post(self, request, *args, **kwargs):
        pass
    pass