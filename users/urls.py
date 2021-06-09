from users.forms import EmailValidationOnForgotPassword
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("signup/", views.sign_up.as_view(), name="signup"),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
]
