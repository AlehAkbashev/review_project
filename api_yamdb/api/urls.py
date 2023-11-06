from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    MyTokenObtainPairView, ReviewViewSet, TitleViewSet,
                    UserViewSet, user_registration)

router_v1 = DefaultRouter()
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
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


urlpatterns = [
    path("v1/auth/signup/", user_registration),
    path("v1/auth/token/", MyTokenObtainPairView.as_view()),
    path("v1/", include(router_v1.urls)),
]
