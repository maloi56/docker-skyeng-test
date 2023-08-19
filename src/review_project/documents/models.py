from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.loader import render_to_string

from users.models import User


class Document(models.Model):
    NEW = 0
    UPDATED = 1
    DELETED = 2
    REVIEWED = 3

    DOCUMENT_STATUS = ((NEW, 'Новый'),
                       (UPDATED, 'Отредактированный'),
                       (DELETED, 'Удален'),
                       (REVIEWED, 'Проверен'))

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Файл',
                            upload_to='documents',
                            validators=[FileExtensionValidator(allowed_extensions=['py'])],
                            blank=True,
                            null=True)
    filename = models.CharField(max_length=64, default=None, blank=True, null=True)
    status = models.SmallIntegerField(choices=DOCUMENT_STATUS, default=NEW)
    updated = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True)

    def __str__(self):
        return f'id - {self.pk}, owner - {self.owner}, filename - {self.file}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.filename:
            self.filename = Path(self.file.name).name
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class Codereview(models.Model):
    document = models.OneToOneField(to=Document, verbose_name=("Файл"), on_delete=models.CASCADE, related_name='review')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    review = models.TextField(verbose_name='Отчет')
    emailed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return f'Отчет для {self.document}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        file = Document.objects.get(pk=self.document.pk)
        file.status = Document.REVIEWED
        file.save()
        if not Codereview.objects.filter(document=file).exists():
            self.emailed = not file.owner.accept_emails
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def send_email_notification(self):
        subject = f'Результат проверки файла {self.document.filename} на сайте CodeReview'
        context = {'file_content': self.review}
        html_message = render_to_string('documents/notification_email.html', context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.document.owner.email],
        )
        email.content_subtype = 'html'
        email.send()
        self.emailed = True
        self.save()
