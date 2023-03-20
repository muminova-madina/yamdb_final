from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError(
            'Произведение ещё не вышло.',
            params={'value': value},
        )
