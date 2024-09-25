# Generated by Django 4.2.9 on 2024-09-23 17:17

from django.db import migrations, models
import django.db.models.deletion
import etica_y_valores.complaints.custom_fields
import etica_y_valores.complaints.custom_validators
import etica_y_valores.complaints.models

from ..utils.migration_handlers import insert_initial_data


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CityCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClassificationCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('classification', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComplaintModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', etica_y_valores.complaints.custom_fields.UUIDPrimaryKeyField(
                    default=etica_y_valores.complaints.custom_fields.UUIDPrimaryKeyField.generate_uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('business_unit', etica_y_valores.complaints.custom_fields.EncryptedField()),
                ('place', etica_y_valores.complaints.custom_fields.EncryptedField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('names_involved',
                 etica_y_valores.complaints.custom_fields.EncryptedField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('detailed_description',
                 etica_y_valores.complaints.custom_fields.EncryptedField()),
                ('name', etica_y_valores.complaints.custom_fields.EncryptedField(
                    blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, validators=[
                 etica_y_valores.complaints.custom_validators.validate_custom_email])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(
                    upload_to=etica_y_valores.complaints.models.unique_file_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneTypeCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_type', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriorityCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('priority', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelationCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('relation', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatusCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('complaint_id', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='complaints.complaintmodel')),
                ('phone_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='complaints.phonetypecategorymodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movement', models.CharField(max_length=200)),
                ('complaint_id', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='complaints.complaintmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(insert_initial_data),
    ]
