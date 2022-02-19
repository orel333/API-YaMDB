from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser, ROLE_CHOICES

from rest_framework.relations import SlugRelatedField
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404



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
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', )



class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    
    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Укажите оценку от 1 до 10!')
        return value
    
    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставлять не более одного отзыва!')
        return data

    class Meta:
        fields = ('id', 'title', 'text','score', 'author', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'created', 'pub_date')
        model = Comment