from users import views
from django.urls import path
from rest_auth.views import (
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('user', views.UserView.as_view()),
    path('password/change', PasswordChangeView.as_view()),
    path('CSRFtoken', views.CSRFTokenView.as_view()),
    path('password/reset', PasswordResetView.as_view(), name="password_reset"),
    path('password/reset/confirm', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]