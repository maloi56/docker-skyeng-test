# Generated by Django 4.2.4 on 2023-08-17 11:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_rename_documents_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['py'])], verbose_name='Файл'),
        ),
    ]