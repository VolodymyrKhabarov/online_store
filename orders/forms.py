"""
This module for creation orders forms.
"""

from django import forms

from orders.models import ReturnPurchaseModel, PurchaseModel


class ReturnPurchaseForm(forms.ModelForm):
    """
    A form for creating a ReturnPurchaseModel object.

    This form is based on the ReturnPurchaseModel model and is used to create a new object with empty fields.
    """

    class Meta:
        model = ReturnPurchaseModel
        fields = []


class PurchaseForm(forms.ModelForm):
    """
    A form for purchasing a product.
    """

    class Meta:
        model = PurchaseModel
        fields = ["amount"]
