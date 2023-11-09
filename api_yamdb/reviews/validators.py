from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Валидатор для года.
    Проверяет, что год не превышает текущий год.
    """

    current_year = dt.now().year
    if value >= current_year:
        raise ValidationError("The year must be current or less")
