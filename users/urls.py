"""
Users application URL Configuration
"""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", LoginView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout")
]
