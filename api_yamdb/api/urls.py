from django.urls import include, path
<<<<<<< HEAD


from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .routers import CustomRouter
from .views import (
    APISignupView, TokenView, UserViewSet, CategoryViewSet, GenreViewSet, MyUserViewSet, TitleViewSet
)

router_v1_a = CustomRouter()
router_v1_a.register(r'users', UserViewSet)
router_v1_b = routers.DefaultRouter()
router_v1_b.register(r'categories', CategoryViewSet, basename='categories')
router_v1_b.register(r'genres', GenreViewSet, basename='genres')
router_v1_b.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1_a.urls)),
    path('v1/auth/signup/', APISignupView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router_v1_b.urls)),
]
