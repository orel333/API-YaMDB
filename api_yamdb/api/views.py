from rest_framework import permissions, viewsets
from reviews.models import Category, Genre, Title
from users.models import CustomUser

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CustomUserSerializer,
                          GenreSerializer, TitleSerializer)

from rest_framework import viewsets
from reviews.models import Comment, Review,Title
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)



class MyUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения API Users."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
 


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

