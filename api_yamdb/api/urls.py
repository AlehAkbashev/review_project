from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
