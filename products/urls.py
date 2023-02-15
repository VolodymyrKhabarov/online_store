"""
Products URL Configuration
"""

from django.urls import path
from products.views import ProductListView, EditProductView


urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("/edit/<int:pk>", EditProductView.as_view(), name="edit_product")
]
