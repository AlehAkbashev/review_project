from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = dt.now().year
    if value > current_year + 1:
        raise ValidationError("The year must be current or less")
