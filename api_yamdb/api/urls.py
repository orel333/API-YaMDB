from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MyUserViewSet, ProfileViewSet, UserSignupViewSet

router_v1 = routers.DefaulRouter()
router_v1.register(r'users', MyUserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', UserSignupViewSet.as_view()),
    path('v1/auth/token/', TokenObtainPairView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/users/me/', ProfileViewSet.as_view())
]
