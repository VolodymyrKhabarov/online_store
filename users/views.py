"""
This module for processing user requests and returning responses.
"""

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


# Define constants for messages
SUCCESS_REGISTRATION_MSG = "You have successfully registered!"


class SignUpView(CreateView):
    """
    This class-based view is used to handle the user signup process.
    """

    form_class = SignUpForm
    success_url = reverse_lazy("signin")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(self.request, SUCCESS_REGISTRATION_MSG)
        return super().form_valid(form)
