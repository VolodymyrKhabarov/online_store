"""
This module for creation orders forms.
"""

from django import forms

from orders.models import ReturnPurchaseModel, PurchaseModel


class ReturnPurchaseForm(forms.ModelForm):
    """
    A form for creating a ReturnPurchaseModel object.

    This form is based on the ReturnPurchaseModel model and is used to create a new object with
    empty fields.
    """

    class Meta:
        """
        Class Meta is used to specify metadata.
        """

        model = ReturnPurchaseModel
        fields = []


class PurchaseForm(forms.ModelForm):
    """
    A form for purchasing a product.
    """

    class Meta:
        """
        Class Meta is used to specify metadata.
        """

        model = PurchaseModel
        fields = ["amount"]

    def clean_amount(self):
        """
        Validates the 'amount' field and raises a ValidationError if it is zero.

        Returns:
            The validated 'amount' value.
        """
        amount = self.cleaned_data.get("amount")
        if amount == 0:
            raise forms.ValidationError("Amount cannot be 0")
        return amount
