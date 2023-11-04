from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Валидатор для поля username в модели User.
    Проверяет, что значение поля username не равно "me".
    Если значение равно "me", генерирует исключение
    ValidationError с сообщением "You can't use that username".
    """
    if value == "me":
        raise ValidationError("You can't use that username")
