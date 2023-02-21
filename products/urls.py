"""
Products URL Configuration
"""

from django.urls import path

from products.views import CreateProductView, EditProductView, ProductListView


urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("add", CreateProductView.as_view(), name="add"),
    path("edit/<int:pk>", EditProductView.as_view(), name="edit_product")
]
