import jwt
from jwt.exceptions import DecodeError
import logging
import re
import sys
import time

from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import SECRET_KEY
from users.models import CustomUser, PreUser, ROLE_CHOICES

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s - строка %(lineno)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
handler.setFormatter(formatter)
logger.disabled = False
logger.debug('Логирование из serializers запущено')


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        # здесь должны быть разные readonly_fields
        # в зависимости от уровня доступа
        #read_only_fields = ('first_name', 'last_name', 'bio', 'role')


    def create(self, validated_data):
        if 'email' in self.initial_data:
            pass
            #отправляем письмо с кодом подтверждения на адрес email
        if 'confirmation_code' in self.initial_data:
            pass
            #проверяем правильность кода,


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreUser
        fields = (
            'username',
            'email'
        )

    def validate_username(self, value):
        user = None
        try:
            user = CustomUser.objects.get(username=value)
        except:
            pass
        if user is not None:
            raise serializers.ValidationError(
                'У нас уже есть пользователь с таким username.'
            )
        # вместо этой конструкции попробовать использовать
        # просто or None
        logger.debug(f'Validate username: value: {value}')
        #if value == 'me':
        match = re.fullmatch(r'^[mM][eE]$', value)
        if match:
            logger.debug(
                'Зафиксировано недопустимое '
                f'me-подобное имя пользователя {value}'
            )
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        logger.debug(f'Валидация username: {user}')
        return value

    def validate_email(self, value):
        user = None
        try:
            user = CustomUser.objects.get(email=value)
        except:
            pass
        if user is not None:
            raise serializers.ValidationError(
                ('У нас уже есть пользователь с таким email.')
            )
        logger.debug(f'Валидация email: {user}')
        return value

class MyTokenObtainSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    #username = serializers.CharField(default=None)
    #confirmation_code = serializers.CharField(default=None)

    def validate(self, data):
        logger.debug(self.initial_data)
        logger.debug('Validation starts...')
        logger.debug(f'Data to validate: {data}')
        username_from_query = self.initial_data.get('username')
        confirmation_code = self.initial_data.get('confirmation_code')
        logger.debug(
            f'Validation: {username_from_query}:\n {confirmation_code}'
        )
        try:
            payload = jwt.decode(
                jwt=confirmation_code,
                key=SECRET_KEY,
                algorithms=['HS256']
            )
        except DecodeError:
            raise serializers.ValidationError(
                'Данный код сфабрикован.'
            )
        email_from_code = payload.get('email')
        username_from_code = payload.get('username')
        timestamp_from_code = payload.get('timestamp')

        preuser = PreUser.objects.get(username=username_from_code)
        email_from_preuser = preuser.email
        now = time.time()
        if username_from_code != username_from_query:
            raise serializers.ValidationError(
                'Похоже на подложный код подтверждения. '
                'Либо Вы сейчас указали не то имя пользователя, '
                'которое указали при получении кода подтверждения.'
            )
        if  email_from_code != email_from_preuser:
            raise serializers.ValidationError(
                'Похоже на подложный код подтверждения.'
            )
        if int(now) < int(timestamp_from_code):
            raise serializers.ValidationError(
                'Данный код сфабрикован.'
            )
        
        custom_user_data = {
            'username': username_from_query,
            'email': email_from_preuser
        }

        newborn = CustomUser.objects.create_user(**custom_user_data)
        token = AccessToken.for_user(newborn)
        logger.debug(dir(token))
        logger.debug(f'Токен из serializers: {token}')

        data = {'token': token}
        preuser.delete()

        return data