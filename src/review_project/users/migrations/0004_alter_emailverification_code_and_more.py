# Generated by Django 4.2.4 on 2023-08-16 22:41

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_username_emailverification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='code',
            field=models.UUIDField(unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='created',
            field=models.DateField(auto_now=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя пользователя'),
        ),
    ]
