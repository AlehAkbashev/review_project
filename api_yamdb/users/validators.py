from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            {
                'error': "You can't use that username"
            }
        )


def validate(self, data):
    user = get_object_or_404(User, username=data['username'])
    if data['confirmation_code'] != user.confirmation_code:
        raise ValidationError('Confirmation code does not match')
    return data
