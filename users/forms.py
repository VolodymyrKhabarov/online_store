"""
This module for creation sign up form.
"""

from django.contrib.auth.forms import UserCreationForm
from users.models import UserModel


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["username", "email", "password1", "password2"]
