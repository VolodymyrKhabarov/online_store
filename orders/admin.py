"""
Module for registration orders models
"""

from django.contrib import admin

from orders.models import PurchaseModel, ReturnPurchaseModel


@admin.register(PurchaseModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ReturnPurchaseModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass
