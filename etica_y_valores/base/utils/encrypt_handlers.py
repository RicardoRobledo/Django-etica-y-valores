import base64

from django.conf import settings

from cryptography.fernet import Fernet, InvalidToken


cipher_suite = Fernet(base64.urlsafe_b64encode(
    settings.SECRET_KEY_FOR_CIPHER.encode()))


def is_encrypted(value):
    """
    Check if the value is encrypted.

    :param value: The value to check.
    """

    try:
        cipher_suite.decrypt(value.encode()).decode()
        return True
    except (InvalidToken, AttributeError):
        return False


def is_file_encrypted(file):
    """
    Verifica si el archivo actual está encriptado intentando desencriptarlo.
    """

    try:
        file.open('rb')
        encrypted_data = file.read()
        file.close()

        cipher_suite.decrypt(encrypted_data)
        return True
    except (InvalidToken, AttributeError):
        return False
