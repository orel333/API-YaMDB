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
#from rest_framework.simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

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
            return (permissions.IsAuthenticated(),)
        if self.suffix == 'users-list' or 'user-detail':
            logger.debug('Запущен эндпойнт users-list или user-detail')
            return (IsAdminUserCustom(),)

    @action(detail=True, url_path='me', methods=['get', 'patch'])
    def getme(self, request):
        user = get_object_or_404(
            CustomUser,
            username=request.user.username
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data)


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
            timestamp = int(time.time())
            dict = {
                'email': email,
                'username': username,
                'timestamp': timestamp
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
                f'по ключу "confirmation_code".\n\n'
                f'\tОбращаем также Ваше внимание, что код '
                'подтверждения действителен в течение суток.'   
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
            logger.debug(timestamp)
            logger.debug(type(timestamp))
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #email = ''
        #username = ''
        # принимает e-mail, username,
        # формирует код подтверждения (JWT с email и username),
        # отправляет код подтверждения на e-mail
        # создает объект preuser


class TokenView(TokenObtainPairView):
#class TokenView(APIView):
        # принимает username, код подтверждения
        # проверяет, что информация верная (user 
        # из токена и юзер в запросе совпадают,
        # email из токена и email из преюзера совпадают,
        # timestamp из токена не пройден), 
        # создаёт пользователя, выдает токен
        # удаляет объект preuser
    # def post(self, request, *args, **kwargs):
        #pass
    def post(self, request):
        rd = request.data
        logger.debug(f'View: request.data: {rd}')

        serializer = MyTokenObtainSerializer(data=rd)
        if serializer.is_valid():
            logger.debug('Serializer is valid')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



