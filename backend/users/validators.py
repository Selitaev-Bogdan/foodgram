import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка никнейма на запрещенные значения и символы."""
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать "me" в качестве никнейма запрещено.'
        )
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Никнейм содержит недопустимые символы.'
        )
    return value
