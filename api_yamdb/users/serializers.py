from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User


class MyTokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('Confirmation code does not match')
        return data
