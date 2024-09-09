import os
import uuid

from django.db import models

from etica_y_valores.base.models import BaseModel

from .custom_fields import UUIDPrimaryKeyField, EncryptedField
from .custom_validators import validate_custom_email


class ChannelCategoryModel(BaseModel):

    channel = models.CharField(max_length=50, null=False)

    def __repr__(self):
        return f'ChannelCategory(id={self.id}, channel={self.channel}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.channel}'


class CityCategoryModel(BaseModel):

    city = models.CharField(max_length=50, null=False)

    def __repr__(self):
        return f'CityCategory(id={self.id}, city={self.city}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.city}'


class ClassificationCategoryModel(BaseModel):

    classification = models.CharField(max_length=50, null=False)

    def __repr__(self):
        return f'ClassificationCategory(id={self.id}, classification={self.classification}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.classification}'


class StatusCategoryModel(BaseModel):

    status = models.CharField(max_length=50, null=False)

    def __repr__(self):
        return f'StatusCategory(id={self.id}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.status}'


class PriorityCategoryModel(BaseModel):

    priority = models.CharField(max_length=30, null=False)

    def __repr__(self):
        return f'PriorityCategory(id={self.id}, priority={self.priority}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.priority}'


class RelationCategoryModel(BaseModel):

    relation = models.CharField(max_length=30, null=False)

    def __repr__(self):
        return f'RelationCategory(id={self.id}, relation={self.relation}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.relation}'


class PhoneTypeCategoryModel(BaseModel):

    phone_type = models.CharField(max_length=30, null=False)

    def __repr__(self):
        return f'PhoneTypeCategory(id={self.id}, phone_type={self.phone_type}, created_at={self.created_at}, updated_at={self.updated_at})'

    def __str__(self):
        return f'{self.phone_type}'


class CommentModel(BaseModel):

    complaint_id = models.CharField(max_length=20)
    user_d = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        # Mostrar un resumen del comentario
        return f"Comment(id={self.id}, complaint_id={self.complaint_id}, user_d={self.user_d}, comment={self.comment[:50]})"


class ComplaintModel(BaseModel):

    id = UUIDPrimaryKeyField()
    business_unit = EncryptedField(null=False, blank=False)
    place = EncryptedField(null=False, blank=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    names_involved = EncryptedField(null=False, blank=False)
    end_date = models.DateField(null=False)

    detailed_description = EncryptedField(null=False, blank=False)
    name = EncryptedField(null=True, blank=True)
    classification_id = models.ForeignKey(
        ClassificationCategoryModel, null=False, on_delete=models.CASCADE)
    relation_id = models.ForeignKey(
        RelationCategoryModel, null=False, on_delete=models.CASCADE)
    city_id = models.ForeignKey(
        CityCategoryModel, null=False, on_delete=models.CASCADE)
    channel_id = models.ForeignKey(
        ChannelCategoryModel, null=False, on_delete=models.CASCADE)
    priority_id = models.ForeignKey(
        PriorityCategoryModel, on_delete=models.CASCADE)
    status_id = models.ForeignKey(
        StatusCategoryModel, on_delete=models.CASCADE)

    # Propiedad para descifrar business_unit
    @property
    def decrypted_business_unit(self):
        return self._meta.get_field('business_unit').decrypt(self.business_unit)

    # Propiedad para descifrar place
    @property
    def decrypted_place(self):
        return self._meta.get_field('place').decrypt(self.place)

    # Propiedad para descifrar names_involved
    @property
    def decrypted_names_involved(self):
        return self._meta.get_field('names_involved').decrypt(self.names_involved)

    # Propiedad para descifrar detailed_description
    @property
    def decrypted_detailed_description(self):
        return self._meta.get_field('detailed_description').decrypt(self.detailed_description)

    # Propiedad para descifrar name
    @property
    def decrypted_name(self):
        return self._meta.get_field('name').decrypt(self.name) if self.name else None

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return (f'Complaint(id={self.id},'
                f'enterprise_relation={self.relation_id},'
                f'city={self.city_id},'
                f'business_unit={self.business_unit},'
                f'place={self.place},'
                f'date={self.date},'
                f'time={self.time},'
                f'names_involved={self.names_involved},'
                f'report_classification={self.classification_id},'
                f'detailed_description={self.detailed_description},'
                f'name={self.name},'
                f'communication_channel={self.channel_id},'
                f'created_at={self.created_at},'
                f'updated_at={self.updated_at})')


class EmailModel(BaseModel):

    email = models.EmailField(validators=[validate_custom_email])
    complaint_id = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Email(email={self.email}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'


class PhoneModel(BaseModel):

    phone_type = models.ForeignKey(
        PhoneTypeCategoryModel, on_delete=models.CASCADE)
    phone_number = models.CharField(null=False, max_length=10)
    complaint_id = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE)

    def __repr__(self):
        return f'Phone(phone_type={self.phone_type}, phone_number={self.phone_number}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'


def unique_file_path(instance, filename):

    ext = filename.split('.')[-1]
    name = '.'.join(filename.split('.')[:-1])
    short_uuid = str(uuid.uuid4())[:4]
    new_filename = f'{name}_{short_uuid}.{ext}'

    return os.path.join('files/', new_filename)


class FileModel(BaseModel):

    file = models.FileField(upload_to=unique_file_path)
    complaint_id = models.ForeignKey(ComplaintModel, on_delete=models.CASCADE)

    def __repr__(self):
        return f'File(file={self.file}, complaint_id={self.complaint_id})'

    def __str__(self):
        return f'{self.id}'
