"""
This module for processing user requests and returning responses.
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


class SignUpView(CreateView):
    """
    This class-based view is used to handle the user signup process.
    """

    form_class = SignUpForm
    success_url = reverse_lazy("signin")
    template_name = "registration/signup.html"
