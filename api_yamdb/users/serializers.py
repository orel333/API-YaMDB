from rest_framework import serializers
from users.models import ROLE_CHOICES, CustomUser


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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')

    def create(self, validated_data):
        if 'email' in self.initial_data:
            pass
            #отправляем письмо с кодом подтверждения на адрес email
        if 'confirmation_code' in self.initial_data:
            pass
            #проверяем правильность кода,


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email'
        )
