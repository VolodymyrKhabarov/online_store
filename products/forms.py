"""
This module for creation products forms.
"""

from django import forms

from products.models import ProductModel, ReturnPurchaseModel


class EditProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ("name", "description", "price", "quantity")


class ReturnPurchaseForm(forms.ModelForm):
    class Meta:
        model = ReturnPurchaseModel
        fields = []


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ("name", "description", "price", "quantity")
