"""
This module for creation orders forms.
"""

from django import forms

from orders.models import ReturnPurchaseModel


class ReturnPurchaseForm(forms.ModelForm):
    class Meta:
        model = ReturnPurchaseModel
        fields = []
