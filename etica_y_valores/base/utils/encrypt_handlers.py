import base64

from django.conf import settings

from cryptography.fernet import Fernet, InvalidToken


def is_encrypted(value):
    """
    Check if the value is encrypted.

    :param value: The value to check.
    """

    cipher_suite = Fernet(base64.urlsafe_b64encode(
        settings.SECRET_KEY_FOR_CIPHER.encode()))

    try:
        cipher_suite.decrypt(value.encode()).decode()
        return True
    except (InvalidToken, AttributeError):
        return False
