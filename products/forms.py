"""
This module for creation products forms.
"""

from django import forms

from products.models import ProductModel


class CreateProductForm(forms.ModelForm):
    """
    A form for creating a new product.

    The form that extends Django's ModelForm.
    """

    class Meta:
        model = ProductModel
        fields = ("name", "description", "price", "quantity")


class EditProductForm(forms.ModelForm):
    """
    A form for editing product details.

    The form that extends Django's ModelForm and allows editing of product details such as name, description,
    price, and quantity.
    """

    class Meta:
        model = ProductModel
        fields = ("name", "description", "price", "quantity")
