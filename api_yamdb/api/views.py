from rest_framework import filters, permissions, viewsets
from reviews.models import Category, Genre, Title
from users.models import CustomUser
from .serializers import CustomUserSerializer

from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class MyUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения API Users."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # pagination_class

    
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
