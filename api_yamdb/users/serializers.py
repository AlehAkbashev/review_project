from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }
