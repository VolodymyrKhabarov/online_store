"""
Module for defining and describing orders models.
"""

from django.conf import settings
from django.db import models

from products.models import ProductModel


class PurchaseModel(models.Model):
    """
    A model representing a purchase made by a user.

    Each instance of this model represents a single purchase of a product by a user.
    It stores the user's ID and the ID of the purchased product, along with the quantity and purchase date/time.
    """

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = "Purchase"
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"


class ReturnPurchaseModel(models.Model):
    """
    A model class representing a purchase return.
    """

    product = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = "Return"
        verbose_name = "Purchase return"
        verbose_name_plural = "Purchases return"
