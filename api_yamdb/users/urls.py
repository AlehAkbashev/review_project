from django.urls import path
from .views import user_registration, MyTokenObtainPairView


urlpatterns = [
    path('signup/', user_registration),
    path('token/', MyTokenObtainPairView.as_view())
]
