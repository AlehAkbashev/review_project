from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    get_patch_me_user,
    UserViewSet
)

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'comments', CommentViewSet, basename='comments')
router_v1.register(r'reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', get_patch_me_user),
]
