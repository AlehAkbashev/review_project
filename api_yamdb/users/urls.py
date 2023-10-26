from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, MeViewSet

router = routers.DefaultRouter()

router.register('users/me', MeViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

#  users/
# users/{username}
# users/{me}