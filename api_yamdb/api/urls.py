from django.urls import include, path

from .routers import CustomRouter
from .views import (
    APISignupView, TokenView, UserViewSet
)

router_v1 = CustomRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignupView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
