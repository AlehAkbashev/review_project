from django.core.exceptions import ValidationError


def validate_username(value):
    if value == "me":
        raise ValidationError("You can't use that username")
