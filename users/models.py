"""
Module for defining and describing users models.
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserModel(AbstractUser):

    wallet = models.FloatField(default=10000.00)

    class Meta:
        "Class Meta is used to provide metadata to the UserModel model"

        db_table = "users"
