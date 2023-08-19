from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from documents.tasks import send_verification_email
from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2', 'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserRegForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        send_verification_email.delay(user.pk)
        return user


class UserProfileForm(UserChangeForm):
    accept_emails = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'width: 20px; height: 20px;'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('accept_emails',)
