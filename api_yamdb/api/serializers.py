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
from .methods import decode, encode, give_jwt_for
from reviews.models import CustomUser, PreUser, ROLE_CHOICES, Category, Genre, Title

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
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='user')

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')


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

class MyTokenObtainSerializer(
    serializers.Serializer,):
    token = serializers.CharField(read_only=True)

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
            payload = decode(confirmation_code)
        except DecodeError:
            raise serializers.ValidationError(
                'Данный код сфабрикован.'
            )
        email_from_code = payload.get('email')
        username_from_code = payload.get('username')
        preuser_object = False
        if CustomUser.objects.filter(username=username_from_query).exists():
            user_object = CustomUser.objects.get(username=username_from_query)
        elif PreUser.objects.filter(username=username_from_query).exists():
            user_object = PreUser.objects.get(username=username_from_query)
            preuser_object = True
        else:
            raise serializers.ValidationError(
                'Отправлен некорректный username.'
            )
        email_from_model = user_object.email
        if username_from_code != username_from_query:
            raise serializers.ValidationError(
                'Похоже на подложный код подтверждения. '
                'Либо Вы сейчас указали не то имя пользователя, '
                'которое указали при получении кода подтверждения.'
            )
        if  email_from_code != email_from_model:
            raise serializers.ValidationError(
                'Похоже на подложный код подтверждения.'
            )

        if preuser_object:
            custom_user_data = {
                'username': username_from_query,
                'email': email_from_model,
            }
            newborn = CustomUser.objects.create_user(**custom_user_data)
            user_object.delete()
            user_object = newborn
        
        token = give_jwt_for(user_object)
        logger.debug(dir(token))
        logger.debug(f'Токен из serializers: {token}')

        data = {'token': token}

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )
