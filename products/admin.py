"""
Module for registration products models
"""

from django.contrib import admin

from products.models import ProductModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass
