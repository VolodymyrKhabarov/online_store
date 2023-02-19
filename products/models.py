"""
Module for defining and describing products models.
"""

from django.db import models
from django.conf import settings


class ProductModel(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Product"
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class PurchaseModel(models.Model):
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
    product = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = "Return"
        verbose_name = "Purchase return"
        verbose_name_plural = "Purchases return"
