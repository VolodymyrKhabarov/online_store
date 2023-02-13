"""
Module for defining and describing products models.
"""

from django.db import models
from django.conf import settings


class ProductModel(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(help_text="Расскажите о товаре")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0, help_text="Количество на складе")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products"
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class PurchaseModel(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = "Purchases"
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"


class ReturnPurchaseModel(models.Model):
    product = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = "Returns"
        verbose_name = "Повернення покупки"
        verbose_name_plural = "Повернення покупок"
