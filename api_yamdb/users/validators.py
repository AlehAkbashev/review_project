from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            {
                'error': "You can't use that username"
            }
        )