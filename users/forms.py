"""
This module for creation sign up form.
"""

from django.contrib.auth.forms import UserCreationForm

from users.models import UserModel


class SignUpForm(UserCreationForm):
    """
    A form for user registration.

    Extends Django's built-in "UserCreationForm".
    The form takes the user's username, email, password and password confirmation as input.
    """

    class Meta:
        """
        Class Meta is used to specify metadata.
        """
        model = UserModel
        fields = ["username", "email", "password1", "password2"]
