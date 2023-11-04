from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Валидатор для года.
    Проверяет, что год не превышает текущий год + 1.
    """

    current_year = dt.now().year
    if value > current_year + 1:
        raise ValidationError("The year must be current or less")
