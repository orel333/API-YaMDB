from rest_framework import filters, permissions, viewsets
from reviews.models import Category, Genre, Title

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =


class TitleViewSet(viewsets.ModelViewSet):
    pass
