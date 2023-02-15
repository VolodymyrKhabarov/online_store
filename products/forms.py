"""
This module for creation products forms.
"""

from django import forms

from products.models import ProductModel


class EditProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ("name", "description", "price", "quantity")
