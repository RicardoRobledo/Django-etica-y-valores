import re

from django.core.exceptions import ValidationError


def validate_custom_email(email):

    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$')

    if not email_pattern.match(email):
        raise ValidationError(
            f'{email} no es un correo electrónico válido. Debe ser un correo electrónico válido con un dominio permitido.'
        )
