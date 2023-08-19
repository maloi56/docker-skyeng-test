from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, ProfileView, RegistrationView,
                         UserLoginView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='verify'),
]
