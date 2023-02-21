"""
Module for defining and describing products models.
"""

from django.db import models


class ProductModel(models.Model):
    """
    A model class representing a product.
    """

    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        """
        Class Meta is used to specify metadata.
        """
        db_table = "Product"
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
