from rest_framework import viewsets
from reviews.models import Category, Genre, Title, Comment, Review, Title
from users.models import CustomUser
from .serializers import (CategorySerializer, CustomUserSerializer,
                          GenreSerializer, TitleSerializer)
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAdminModeratorUserPermission


import logging
import sys

import jwt
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

from .permissions import (IsAdminOrReadOnly, IsAdminUserCustom,
                          IsOwnerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    trailing_slash = '/'

    def get_permissions(self):
        if 'getme' in self.action_map.values():
            return (permissions.IsAuthenticated,)
        if self.suffix == 'users-list' or 'user-detail':
            return (IsAdminUserCustom(),)

    @action(detail=True, url_path='me', methods=['get', 'patch'])
    def getme(self, request):
        user = get_object_or_404(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class APISignupView(APIView):

    def post(self, request):
        #email = ''
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Пользователи оставляют к произведениям текстовые отзывы."""
    serializer_class = ReviewSerializer
    permission_class = (IsAdminModeratorUserPermission,)
    
    def get_queryset(self):
        title = get_object_or_404(
        Title,
        id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Пользователи оставляют коментарии к отзывам."""
    serializer_class = CommentSerializer
    permission_class = (IsAdminModeratorUserPermission,)

        
    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

