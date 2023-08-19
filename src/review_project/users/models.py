from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=150, blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)
    register_date = models.DateTimeField(verbose_name='Дата регистрации', default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    accept_emails = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    code = models.UUIDField(verbose_name='Код', unique=True)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    created = models.DateField(verbose_name='Дата создания', auto_now=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse('users:verify', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.email} на CodeReview'
        context = {
            'user_email': self.user.email,
            'verification_link': verification_link,
        }

        # Сгенерируйте HTML и текстовую версии сообщения
        html_message = render_to_string('users/confirmation_email.html', context)
        # Отправьте письмо
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.user.email],
        )
        email.content_subtype = 'html'
        email.send()

    def is_expired(self):
        return now() >= self.expiration
