from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, MeViewSet, user_registration
from rest_framework_simplejwt.views import TokenObtainPairView


router = routers.DefaultRouter()

router.register('users/me', MeViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('auth/signup/', user_registration),
    path('', include(router.urls)),
]

#  users/
# users/{username}
# users/{me}