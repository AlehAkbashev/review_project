from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    user_registration,
    MyTokenObtainPairView
)


router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/auth/signup/', user_registration),
    path('v1/auth/token/', MyTokenObtainPairView.as_view()),
    path('v1/', include(router_v1.urls)),
]
