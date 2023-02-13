"""
Module for registration products models
"""

from django.contrib import admin
from products.models import ProductModel, PurchaseModel, ReturnPurchaseModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(PurchaseModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ReturnPurchaseModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass
