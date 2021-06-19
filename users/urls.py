from django.contrib.auth import views as auth_views
from django.urls import path

from users.forms import EmailValidationOnForgotPassword

from . import views

urlpatterns = [
    path('signup/', views.sign_up.as_view(), name='signup'),

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=EmailValidationOnForgotPassword),
        name='password_reset'),
]
