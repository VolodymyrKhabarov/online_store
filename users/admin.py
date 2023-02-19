"""
Module for registration users models
"""

from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass
