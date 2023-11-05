from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    MyTokenObtainPairView,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    user_registration
)

router_v1 = DefaultRouter()
router_v1.register("categories", CategoriesViewSet, basename="categories")
router_v1.register(r"genres", GenresViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

v1_urls = [
    path("auth/signup/", user_registration),
    path("auth/token/", MyTokenObtainPairView.as_view()),
    path("", include(router_v1.urls)),
]

urlpatterns = [
    path("v1/", include((v1_urls, "v1"))),
]
