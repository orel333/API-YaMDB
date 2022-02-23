import jwt
import logging
import sys
import time

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .methods import get_user_role
from .serializers import (
    CustomUserSerializer,
    SignUpSerializer,
    MyTokenObtainSerializer,
)
from api_yamdb.settings import SECRET_KEY
from users.models import CustomUser


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    trailing_slash = '/'

    def get_permissions(self):
        if 'getme' in self.action_map.values():
            logger.debug('Запущен эндпойнт me')
            return (permissions.IsAuthenticated(),)
        if self.suffix == 'users-list' or 'user-detail':
            logger.debug('Запущен эндпойнт users-list или user-detail')
            return (IsAdminUserCustom(),)

    @action(detail=True, url_path='me', methods=['get', 'patch'])
    def getme(self, request):
        request_user = request.user
        custom_user = CustomUser.objects.get(username=request_user.username)
        logger.debug(request.auth)

        if request.method == 'GET':
            serializer = self.get_serializer(custom_user)
            logger.debug('Зафиксирован метод GET')
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            request_user_role = get_user_role(request.auth)
            logger.debug(f'User role: {request_user_role}')
            rd = request.data
            if 'role' in rd:
                del rd['role']
            #rd['role'] = request_user_role
            if 'username' not in rd:
                rd['username'] = request_user.username
            if 'email' not in rd:
                rd['email'] = request_user.email
            serializer = self.get_serializer(custom_user, data=rd)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_200_OK)
            


class APISignupView(APIView):

    def post(self, request):
        logger.debug(request.data)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug('Валидация APISignupView пройдена')
            serializer.save()
            email = request.data.get('email')
            username = request.data.get('username')
            logger.debug(f'{username}: {email}')
            dict = {
                'email': email,
                'username': username,
            }
            key = SECRET_KEY
            encoded = jwt.encode(dict, key, 'HS256')
            mail_theme = 'Подтверждение регистрации пользователя'
            mail_text = (
                f'Здравствуйте!\n\n\tВы (или кто-то другой) '
                'запросили регистрацию на сайте YaMDB. '
                'Для подтверждения регистрации отправьте POST запрос '
                'на адрес: http://127.0.0.1/api/v1/auth/token/. '
                f'В теле запроса передайте имя пользователя {username} '
                f'по ключу "username" и код \n\n{encoded}\n\n'
                f'по ключу "confirmation_code".'
            )
            mail_from = 'orel333app@gmail.com'
            mail_to = [email]
            send_mail(
                mail_theme,
                mail_text,
                mail_from, 
                mail_to,
                fail_silently=False
            )
            logger.debug(encoded)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(TokenObtainPairView):
    def post(self, request):
        rd = request.data
        logger.debug(f'View: request.data: {rd}')

        serializer = MyTokenObtainSerializer(data=rd)
        if serializer.is_valid():
            logger.debug('Serializer is valid')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



