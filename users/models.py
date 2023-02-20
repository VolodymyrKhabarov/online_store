"""
Module for defining and describing users models.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    """
    Custom user model that extends Django's built-in User model
    with a wallet attribute to track user balance.
    """

    wallet = models.FloatField(default=10000.00)

    class Meta:
        """
        Class Meta is used to specify metadata.
        """
        db_table = "User"
