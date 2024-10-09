import uuid
import base64

from django.db import models
from django.conf import settings

from etica_y_valores.base.utils.encrypt_handlers import cipher_suite


class UUIDPrimaryKeyField(models.Field):
    """
    A custom field that uses UUID as a primary key, stored in uppercase and without hyphens.
    """

    description = "A primary key field that uses UUID in uppercase without hyphens"

    def __init__(self, *args, **kwargs):
        # Ensure this field is set as the primary key and unique
        kwargs['primary_key'] = True
        kwargs['unique'] = True
        # Automatically generate a UUID without hyphens as the default value
        kwargs['default'] = self.generate_uuid
        # Make this field non-editable since it will be generated automatically
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def generate_uuid(self):
        """
        Generate a UUID, remove hyphens, and convert it to uppercase.
        """

        return uuid.uuid4().hex.upper()

    def db_type(self, connection):
        """
        Define the database type as a 32-character string (no hyphens, uppercase).
        """

        # UUID will be stored as a 32-character string (hexadecimal, no hyphens)
        return 'char(32)'

    def get_prep_value(self, value):
        """
        Ensure the value is prepared correctly before saving to the database (uppercase, no hyphens).
        """

        return str(value).replace('-', '').upper()


class EncryptedField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.cipher_suite = cipher_suite
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return value
        return self.cipher_suite.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        # No descifrar automáticamente cuando se accede desde el admin
        return value

    def decrypt(self, value):
        # Método para descifrar manualmente el valor
        if not value:
            return value
        return self.cipher_suite.decrypt(value.encode()).decode()
