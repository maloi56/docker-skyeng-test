# Generated by Django 4.2.4 on 2023-08-17 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_rename_file_codereview_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codereview',
            old_name='is_emailed',
            new_name='emailed',
        ),
    ]
