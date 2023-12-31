import uuid
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView, UpdateView

from common.view import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegForm
from users.models import EmailVerification, User


class IndexView(TitleMixin, TemplateView):
    template_name = 'index.html'
    title = 'CodeReview'


class ProfileView(SuccessMessageMixin, TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')
    title = 'CodeReview - Личный кабинет'
    success_message = 'Данные успешно обновлены!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.pk,))

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.pk:
            return HttpResponseRedirect(reverse_lazy('users:profile', args=(self.request.user.pk,)))
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        error(self.request, form.errors)
        return super().form_invalid(form)


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    title = 'CodeReview - Авторизация'


class RegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
    success_message = 'Для заверешения регистрации на вашу почту отправлено письмо с подтверждением'
    title = 'CodeReview - Регистрация'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'CodeReview - Подтверждение электронной почты'
    is_success = True

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verify = EmailVerification.objects.filter(user=user, code=code)

        if email_verify.exists() and not user.is_verified_email:
            if not email_verify.first().is_expired():
                user.is_verified_email = True
                user.save()
                email_verify.first().delete()
                return super().get(request, *args, **kwargs)
            else:
                email_verify.first().delete()
                expiration = now() + timedelta(hours=48)
                new_email_verify = EmailVerification.objects.create(code=uuid.uuid4(), expiration=expiration, user=user)
                new_email_verify.send_verification_email()
                self.is_success = False
                return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_success'] = self.is_success
        return context
