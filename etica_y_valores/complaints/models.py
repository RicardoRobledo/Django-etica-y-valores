import re
import uuid

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.utils import timezone


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


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Complaint(BaseModel):

    id = UUIDPrimaryKeyField()
    enterprise_relation = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
        null=False
    )
    city = models.CharField(
        max_length=70,
        validators=[MaxLengthValidator(70)],
        null=False
    )
    business_unit = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
        null=False
    )
    place = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
        null=False
    )
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    names_involved = models.TextField(
        null=False
    )
    report_classification = models.CharField(
        max_length=70,
        validators=[MaxLengthValidator(70)],
        null=False
    )
    detailed_description = models.TextField(null=False,)
    name = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50)],
        null=False
    )
    communication_channel = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50)],
        null=False
    )

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return (f'Complaint(id={self.id},'
                f'enterprise_relation={self.enterprise_relation},'
                f'city={self.city},'
                f'business_unit={self.business_unit},'
                f'place={self.place},'
                f'date={self.date},'
                f'time={self.time},'
                f'names_involved={self.names_involved},'
                f'report_classification={self.report_classification},'
                f'detailed_description={self.detailed_description},'
                f'name={self.name},'
                f'communication_channel={self.communication_channel},'
                f'created_at={self.created_at},'
                f'updated_at={self.updated_at})')


def validate_custom_email(email):

    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|mil|int)$')

    if not email_pattern.match(email):
        raise ValidationError(
            f'{email} no es un correo electrónico válido. Debe ser un correo electrónico válido con un dominio permitido.'
        )


class Email(BaseModel):

    email = models.EmailField(validators=[validate_custom_email])
    complaint_id = models.ForeignKey(Complaint, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Email(email={self.email}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'


class Phone(BaseModel):

    phone_type = models.CharField(null=False, max_length=30)
    phone_number = models.CharField(null=False, max_length=10)
    complaint_id = models.ForeignKey(Complaint, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Phone(phone_type={self.phone_type}, phone_number={self.phone_number}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'


def unique_file_path(instance, filename):
    import os
    # Extrae la extensión del archivo original
    ext = filename.split('.')[-1]
    # Genera un nombre de archivo único usando uuid4
    filename = f'{uuid.uuid4()}.{ext}'
    # Devuelve el path completo, donde 'files/' es el directorio de destino
    return os.path.join('files/', filename)


class File(BaseModel):

    file = models.FileField(upload_to='files/')
    complaint_id = models.ForeignKey(Complaint, on_delete=models.CASCADE)

    def __repr__(self):
        return f'File(file={self.file}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'
