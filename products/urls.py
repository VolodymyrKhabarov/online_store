"""
Products URL Configuration
"""

from django.urls import path

from products.views import CreateProductView, ProductListView, EditProductView, PurchaseListView, RefundListView


urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("edit/<int:pk>", EditProductView.as_view(), name="edit_product"),
    path("orders", PurchaseListView.as_view(), name="orders"),
    path("add", CreateProductView.as_view(), name="add"),
    path("refunds", RefundListView.as_view(), name="refunds")
]
