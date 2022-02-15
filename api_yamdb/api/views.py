from rest_framework import viewsets

from users.models import CustomUser
from .serializers import CustomUserSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения API Users."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # pagination_class
