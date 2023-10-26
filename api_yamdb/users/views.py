from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UsersSerializer
import secrets


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pass


class MeViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pass


# create code confirmation
# send email
# create jwt get token
# update jwt token