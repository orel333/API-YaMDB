from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CategoryViewSet, GenreViewSet, MyUserViewSet, TitleViewSet
from .views import ReviewViewSet, CommentViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', MyUserViewSet, basename='user')

router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='review'
    )
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)



urlpatterns = [
  
    path('v1/', include(router_v1.urls)),
]
