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
